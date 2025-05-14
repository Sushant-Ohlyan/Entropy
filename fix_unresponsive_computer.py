import subprocess
import time
subprocess.call('taskkill /IM explorer.exe /F', shell=True)
time.sleep(2)
subprocess.call(["start", "explorer.exe"], shell=True)