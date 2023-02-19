from lib.cipher import AESCipher
from colorama import Fore, Back, Style, init
from time import sleep
import json
import re
import lib.getpass_ak as getpass_ak

"""
pyinstaller --onefile -n "MakeEncFile.exe" "MakeEncryptFile.py"
"""


schedule_xml = dict(
    workin = r"""
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Date>2020-01-06T16:51:37.069071</Date>
    <Author>DESKTOP-TKJ61EM\h</Author>
    <Description>AutoWorkIn</Description>
    <URI>\AutoWorkIn</URI>
  </RegistrationInfo>
  <Triggers>
    <CalendarTrigger>
      <StartBoundary>2020-01-06T09:15:00</StartBoundary>
      <ExecutionTimeLimit>PT1H</ExecutionTimeLimit>
      <Enabled>true</Enabled>
      <ScheduleByDay>
        <DaysInterval>1</DaysInterval>
      </ScheduleByDay>
    </CalendarTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <UserId>S-1-5-18</UserId>
      <RunLevel>LeastPrivilege</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>true</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>true</StopIfGoingOnBatteries>
    <AllowHardTerminate>false</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>true</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <DisallowStartOnRemoteAppSession>false</DisallowStartOnRemoteAppSession>
    <UseUnifiedSchedulingEngine>true</UseUnifiedSchedulingEngine>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT1H</ExecutionTimeLimit>
    <Priority>7</Priority>
    <RestartOnFailure>
      <Interval>PT1M</Interval>
      <Count>3</Count>
    </RestartOnFailure>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>C:\Users\h\Documents\GitHub\project\chulcheck\dist\AutoAttendance.exe</Command>
      <WorkingDirectory>C:\Users\h\Documents\GitHub\project\chulcheck\dist</WorkingDirectory>
    </Exec>
  </Actions>
</Task>    
    """,
    workout = r"""
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Date>2020-01-06T16:54:10.6254723</Date>
    <Author>DESKTOP-TKJ61EM\h</Author>
    <Description>AutoWorkOut</Description>
    <URI>\AutoWorkOut</URI>
  </RegistrationInfo>
  <Triggers>
    <CalendarTrigger>
      <StartBoundary>2020-01-06T18:30:00</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByDay>
        <DaysInterval>1</DaysInterval>
      </ScheduleByDay>
    </CalendarTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <UserId>S-1-5-18</UserId>
      <RunLevel>LeastPrivilege</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>true</StopIfGoingOnBatteries>
    <AllowHardTerminate>false</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>true</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <DisallowStartOnRemoteAppSession>false</DisallowStartOnRemoteAppSession>
    <UseUnifiedSchedulingEngine>true</UseUnifiedSchedulingEngine>
    <WakeToRun>true</WakeToRun>
    <ExecutionTimeLimit>PT1H</ExecutionTimeLimit>
    <Priority>7</Priority>
    <RestartOnFailure>
      <Interval>PT1M</Interval>
      <Count>3</Count>
    </RestartOnFailure>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>C:\Users\h\Documents\GitHub\project\chulcheck\dist\AutoAttendance.exe</Command>
      <WorkingDirectory>C:\Users\h\Documents\GitHub\project\chulcheck\dist</WorkingDirectory>
    </Exec>
  </Actions>
</Task>    
    """
)


if __name__ == '__main__':
    init(autoreset=True)
    print(Fore.GREEN + '* Server Setting')
    print(Fore.GREEN + f' \n # Login ID')
    user_id = str(input('   id   : ') or '').strip()
    if user_id == '':
        print(Back.RED + f'"ID" required')
        sleep(10)
        exit()

    print(Fore.GREEN + f' \n # Login PW')
    user_password = str(getpass_ak.getpass(prompt='   pw   : ', stream=None) or '').strip()
    if user_password == '':
        print(Back.RED + f'"password" required')
        sleep(10)
        exit()

    print(Fore.GREEN + f' \n # User CODE')
    user_code = str(input('   code : ') or '').strip()
    if user_code == '' or not re.match(r'\d+', user_code):
        print(Back.RED + f'"code number" required')
        sleep(10)
        exit()

    (work_in_start, work_in_end) = ('09:20:00', '09:28:00')
    print(Fore.GREEN + f' \n # WorkIn Time Range(24h): default({work_in_start} ~ {work_in_end})')
    work_in_time_range = str(input('   WorkIn Time Range : ') or '').strip()
    work_in_time_range = work_in_time_range if not(work_in_time_range is None or work_in_time_range == '') else f'{work_in_start} ~ {work_in_end}'
    work_in_search = re.search(r"(\d{2}:\d{2}:\d{2})[ \t]*~[ \t]*(\d{2}:\d{2}:\d{2})", work_in_time_range)
    if work_in_search and work_in_search.group(1) and work_in_search.group(2):
        (work_in_start, work_in_end) = (work_in_search.group(1), work_in_search.group(2))
    else:
        print(Fore.LIGHTRED_EX + f'\tWorkIn set fail: Using auto set')
    print(Fore.LIGHTCYAN_EX + f'\tWorkIn set:\n\t\tWorkIn Start : {work_in_start}\n\t\tWorkIn End   : {work_in_end}')

    (work_out_start, work_out_end) = ('18:45:00', '19:15:00')
    print(Fore.GREEN + f' \n # WorkOut Time Range(24h): default({work_out_start} ~ {work_out_end})')
    work_out_time_range = str(input('   WorkOut Time Range : ') or '').strip()
    work_out_time_range = work_out_time_range if not(work_out_time_range is None or work_out_time_range == '') else f'{work_out_start} ~ {work_out_end}'
    work_out_search = re.search(r"(\d+:\d+:\d+)[ \t]*~[ \t]*(\d+:\d+:\d+)", work_out_time_range)
    if work_out_search and work_out_search.group(1) and work_out_search.group(2):
        (work_out_start, work_out_end) = (work_out_search.group(1), work_out_search.group(2))
    else:
        print(Fore.LIGHTRED_EX + f'\tWorkOut set fail: Using auto set')
    print(Fore.LIGHTCYAN_EX + f'\tWorkOut set:\n\t\tWorkOut Start : {work_out_start}\n\t\tWorkOut End   : {work_out_end}')

    print(Fore.GREEN + f' - Slack Channel ID')
    slack_channel = str(input('slackId : ') or '').strip()

    user_info = dict(
        user_id=user_id,
        user_password=user_password,
        user_code=user_code,
        work_in=dict(
            start=work_in_start,
            end=work_in_end,
        ),
        work_out=dict(
            start=work_out_start,
            end=work_out_end,
        ),
        slack_channel=slack_channel
    )

    cipher_instance = AESCipher()

    # 암호화를 합니다.
    encrypted = cipher_instance.encrypt(json.dumps(user_info))
    with open('UserEncFile', 'w') as UserEncFile:
        UserEncFile.write(encrypted)

    # print('암호화된 값 : ' + encrypted_1)

    # encrypted_2 = cipherinstance.encrypt(r'ssrinc!123')
    # print('암호화된 값 : ' + encrypted_2)

    # # 암호화 한 값을 다시 복호화 합니다.
    # decrypted = cipherinstance.decrypt(encrypted_1)
    # print('복호화된 값 : ' + decrypted)
