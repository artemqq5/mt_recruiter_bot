import os
import time

while True:
    print('start')
    try:
        os.system("python3 /home/ftpuser/mt_recruiter_bot/main.py")
    except Exception as e:
        print(f'exception in start: {e}')
    print('crash')
    time.sleep(5)
   