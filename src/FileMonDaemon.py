import logging
import daemon
import sys
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def DirectoryMonitor(DirPath):
    def on_any_event(event):
      print(event)
      
    path = DirPath if len(DirPath) > 1 else '.'
    event_handler = FileSystemEventHandler()
    event_handler.on_any_event = on_any_event
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
        
with daemon.DaemonContext():
    DirPath = '/home/ec2-user/environment/EncryptedBackupService/Encrypted-Backup-Service/TestDir/'
    DirectoryMonitor(DirPath)
'''
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
'''