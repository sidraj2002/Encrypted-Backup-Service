'''Input: FilePath, EncryptionKeyID, SecretsManager
Description: Ingest Files, fetch existing key from secrets manager and encypt files
'''
import boto3
import sys
import os
import subprocess
import cryptography
import base64
import datetime
from botocore.exceptions import ClientError
from cryptography.fernet import Fernet

class SymmetricKey:
    def __init__(self):
        self.KeyName = None
        self.KeyValue = None
        self.KeyType = None
        self.KeyTimeStamp = None
        
'''Generate new Key at the OS level and Return Key object'''        
def GenerateKey(KeyName):
    NewKey = SymmetricKey()
    Key = Fernet.generate_key()
    #print(Key)
    NewKey.KeyName = KeyName
    NewKey.KeyValue = Key
    NewKey.KeyType = 'Fernet'
    NewKey.KeyTimeStamp = datetime.datetime.now()
    return NewKey
 
'''Upload generated Key.Value to AWS Secrets Manager'''    
def SecretsManagerAWS(KeyObject):
    try:
        client = boto3.client('secretsmanager')
        response = client.get_secret_value(
        SecretId=KeyObject.KeyName
        )
    except ClientError as error:
        #print(error.response)
        KeyVal = KeyObject.KeyValue
        response = client.create_secret(
        Name=KeyObject.KeyName,
        Description='Sids Utility Generated Secret',
        SecretString=base64.b64encode(KeyVal),
        Tags=[
           {
                'Key': 'CreationTimeStamp',
                'Value': str(KeyObject.KeyTimeStamp)
             },
          ],
          ForceOverwriteReplicaSecret=True
        )
    #print(response)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        #print(response)
        return response
    else:
        
        return (response)
        
def EncryptFiles(SecretString, FilePath):
    
    encrypt = Fernet(SecretString)
    with open(FilePath, 'rb') as f:
        data = f.read()
        encrypted = encrypt.encrypt(data)

        output_file = FilePath + '.encrypted'
    with open(output_file, 'wb') as f:
        f.write(encrypted)
        
def DecryptFiles(SecretBinary, FilePath):
    
    decrypt = Fernet(SecretBinary)
    with open(FilePath, 'rb') as f:
        data = f.read()
        decrypted = decrypt.decrypt(data)

        output_file = FilePath + '.decrypted'
    with open(output_file, 'wb') as f:
        f.write(decrypted)
'''If KeyName environment variable exists, pull key value from secrets manager; If it doesnt exist, create new key, push to secrets manager'''
'''Only KeyName is stored at the OS level; So auth needs to be done through AWS to retrieve actual key from secrets manager'''
'''Exporting Key Name to OS still needs to be done - Subprocess or something like that'''

try: 
    if os.getenv('KeyName') is None:
        key = GenerateKey('MyNewKey1')
        #print(key.KeyValue)
        response = SecretsManagerAWS(key)
        #print(response['ARN'])
    else:
        print('Key already Exists: ', os.getenv('KeyName'))
        key = SymmetricKey()
        key.KeyName = os.getenv('KeyName')
        response = SecretsManagerAWS(key)
        #print(response)

except ClientError as error:
        print(error.response)        
# KMSKeyID - Add to Config File
key = response['SecretBinary']
print(key)
#key = key.encode('utf-8')
#newkey = base64.b64decode(key)
#print(newkey)

EncryptFiles(key, '/home/ec2-user/environment/EncryptDaemon/Encrypted-Backup-Service/TestDir/Untitled')
DecryptFiles(key, '/home/ec2-user/environment/EncryptDaemon/Encrypted-Backup-Service/TestDir/Untitled.encrypted')