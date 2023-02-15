from __future__ import annotations

import asyncio
import base64
import logging
from binascii import unhexlify
from functools import wraps
from typing import Any, Callable, Coroutine, Iterable, List, Protocol, Union

import grpc
from Crypto.Cipher import AES  # type: ignore[import]  # noqa: S413
from asgiref.sync import SyncToAsync
from buzzvil_billing.billing_pb2_grpc import BillingServiceServicer
from ddtrace import tracer
from django.db import close_old_connections, connection
from google.protobuf import json_format
from google.protobuf.message import Message

logger = logging.getLogger(__name__)


class RequestHandler(Protocol):
    def __call__(
        self,
        __self: BillingServiceServicer,
        request: Message,
        context: grpc.ServicerContext,
    ) -> Message:
        ...


def trace_request(logger: logging.Logger = logger) -> Callable[[RequestHandler], RequestHandler]:
    def decorator(func: RequestHandler) -> RequestHandler:
        @wraps(func)
        def inner(
            self: BillingServiceServicer,
            request: Message,
            context: grpc.ServicerContext,
        ) -> Message:
            peer = context.peer()
            request_name = request.DESCRIPTOR.name
            request_body = json_format.MessageToDict(
                request, preserving_proto_field_name=True, use_integers_for_enums=True
            )
            log_str = f'{request_name} from {peer} {request_body}'

            logger.info(log_str)

            span = tracer.current_span()
            if span:
                span.set_tag(key='grpc.request', value=request_body)

            response = func(self, request, context)  # noqa: FKA100
            return response

        return inner

    return decorator


def _async_run_tasks(coroutines: Iterable[Coroutine[Any, Any, None]], concurrent_tasks_limit: int) -> None:
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    task = loop.create_task(
        _async_gather_with_semaphore(
            coroutines=coroutines,
            concurrent_tasks_limit=concurrent_tasks_limit,
        )
    )
    loop.run_until_complete(task)


async def _async_gather_with_semaphore(
    coroutines: Iterable[Coroutine[Any, Any, None]], concurrent_tasks_limit: int
) -> None:
    semaphore = asyncio.Semaphore(concurrent_tasks_limit)

    async def _with_semaphore(coroutine: Coroutine[Any, Any, None]) -> None:
        async with semaphore:
            await coroutine

    await asyncio.gather(*(_with_semaphore(c) for c in coroutines))


class PKCS7Encoder:
    def __init__(self) -> None:
        self.block_size = 16

    def encode(self, text: str) -> bytes:
        text_length = len(text.encode())
        amount_to_pad = self.block_size - (text_length % self.block_size)
        if amount_to_pad == 0:
            amount_to_pad = self.block_size
        pad = unhexlify("%02x" % amount_to_pad)
        return text.encode() + pad * amount_to_pad

    def decode(self, text: Union[str, bytes]) -> str:
        if isinstance(text, bytes):
            text = text.decode()
        pad = ord(text[-1])
        return text[:-pad]


def encrypt_aes(original_text: str, key: str, iv: str) -> bytes:
    blocked_text = PKCS7Encoder().encode(original_text)

    aes = AES.new(key, AES.MODE_CBC, iv)  # noqa: FKA100
    encrypted_text = aes.encrypt(blocked_text)

    base64_encrypted_text = base64.b64encode(encrypted_text)
    return base64_encrypted_text


def decrypt_aes(base64_encrypted_text: str, key: str, iv: str) -> str:
    encrypted_text = base64.b64decode(base64_encrypted_text)

    aes = AES.new(key, AES.MODE_CBC, iv)  # noqa: FKA100
    blocked_text = aes.decrypt(encrypted_text)

    original_text = PKCS7Encoder().decode(blocked_text)
    return original_text


class DatabaseSyncToAsync(SyncToAsync):
    """
    SyncToAsync version that cleans up old database connections when it exits.
    """

    def thread_handler(self, loop: Any, source_task: Any, exc_info: Any, func: Any, *args: Any, **kwargs: Any) -> Any:
        close_old_connections()
        try:
            return super().thread_handler(  # type: ignore[no-untyped-call] # noqa: FKA100
                loop,
                source_task,
                exc_info,
                func,
                *args,
                **kwargs,
            )
        finally:
            close_old_connections()


database_sync_to_async = DatabaseSyncToAsync


def execute_query(query: str) -> List[Any]:
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
    return rows  # type: ignore[no-any-return]