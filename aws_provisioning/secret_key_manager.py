''' Generate key and push to AWS secrets manager and export environment variables'''
import boto3
import base64
import sys
import os
import subprocess
import cryptography
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
        SecretBinary=KeyVal,
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
'''If KeyName environment variable exists, pull key value from secrets manager; If it doesnt exist, create new key, push to secrets manager'''
'''Only KeyName is stored at the OS level; So auth needs to be done through AWS to retrieve actual key from secrets manager'''
'''Exporting Key Name to OS still needs to be done - Subprocess or something like that'''

try: 
    if os.getenv('KeyName') is None:
        key = GenerateKey('MyNewKey1')
        #print(key.KeyValue)
        response = SecretsManagerAWS(key)
        print(response)
    else:
        print('Key already Exists: ', os.getenv('KeyName'))
        key = SymmetricKey()
        key.KeyName = os.getenv('KeyName')
        response = SecretsManagerAWS(key)
        #print(response)
    

except ClientError as error:
        print(error.response)        
# KMSKeyID - Add to Config File 
