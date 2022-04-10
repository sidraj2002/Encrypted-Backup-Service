import logging
import daemon
import sys
import os
import time
from botocore.exceptions import ClientError
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
sys.path.append('/home/ec2-user/environment/EncryptedBackupService/Encrypted-Backup-Service/aws_provisioning/')
from secret_key_manager import SecretsManagerAWS
from secret_key_manager import GenerateKey
from secret_key_manager import SymmetricKey

def DirectoryMonitor(DirPath):
    def on_created(event):
      print(event)
      file = open('/home/ec2-user/environment/EncryptedBackupService/Encrypted-Backup-Service/event.txt', 'w')
      file.writelines(event.src_path)
      file.close()
      
    path = DirPath if len(DirPath) > 1 else '.'
    event_handler = FileSystemEventHandler()
    event_handler.on_created = on_created
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()


try: 
    if os.getenv('KeyName') is None:
        print('Key does not exist: Creating new one')
        key = GenerateKey('MyNewKey')
        #print(key.KeyValue)
        response = SecretsManagerAWS(key)
        print(response)
    else:
        print('Key already Exists: ', os.getenv('KeyName'))
        key = SymmetricKey()
        key.KeyName = os.getenv('KeyName')
        response = SecretsManagerAWS(key)
        print(response)
    

except ClientError as error:
        print(error.response) 
       
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