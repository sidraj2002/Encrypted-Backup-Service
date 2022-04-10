import logging
import daemon
import sys
import time
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import os
import grp
import signal
import daemon
import lockfile


import FileEncrypter
count = 0
with daemon.DaemonContext():
  while 1:
        print('Hello-World')
        command = "touch /home/ec2-user/environment/EncryptedBackupService/Encrypted-Backup-Service/testfile" + str(count)
        os.system(command)
        time.sleep(1)
        command = "rm -rf /home/ec2-user/environment/EncryptedBackupService/Encrypted-Backup-Service/testfile" + str(count)
        os.system(command)
        count = count+1
        time.sleep(1)
