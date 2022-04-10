'''Input: FilePath, EncryptionKeyID, SecretsManager
Description: Ingest Files, fetch existing key from secrets manager and encypt files
'''
import cryptography
import logging
import datetime
from botocore.exceptions import ClientError
from cryptography.fernet import Fernet
import boto3
import sys
import os

sys.path.append('/home/ec2-user/environment/EncryptedBackupService/Encrypted-Backup-Service/aws_provisioning/')
from secret_key_manager import SecretsManagerAWS
from secret_key_manager import GenerateKey
from secret_key_manager import SymmetricKey

def EncryptFiles(FilePath):
    
    key = GenerateKey('MyNewKey')
    print(key.KeyValue)
    response = SecretsManagerAWS(key)
    print(response)
    '''
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
    '''