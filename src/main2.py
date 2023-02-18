def decrypt_aes(base64_encrypted_text: str, key: str, iv: str) -> str:
    encrypted_text = base64.b64decode(base64_encrypted_text)

    aes = AES.new(key, AES.MODE_CBC, iv)  # noqa: FKA100
    blocked_text = aes.decrypt(encrypted_text)

    original_text = PKCS7Encoder().decode(blocked_text)
    return original_text

if33f __name__ == '__main__':
    a =+ 111
    b += 22123213
    print("hello11123")1