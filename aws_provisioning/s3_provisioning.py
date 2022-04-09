import boto3
import sys
import os
import subprocess
from botocore.exceptions import ClientError

s3 = boto3.client('s3')

def s3CreateBuckets(region, BucketName):
    CreateBucket = s3.create_bucket(Bucket=BucketName,CreateBucketConfiguration={
        'LocationConstraint': region,
    })
    #response = s3.list_buckets()
    
    return CreateBucket
    
''' Create S3 Buckt if the environment variable doesnt exist. Then Set env variable with Bucket name and URL '''   
 
try:
    if sys.argv != None and os.getenv('S3BUCKETURL') is None:
        print(os.getenv('S3BUCKETURL'))
        newbucket = s3CreateBuckets(sys.argv[1], sys.argv[2])
        #print(newbucket['ResponseMetadata'])
        if newbucket['ResponseMetadata']['HTTPStatusCode'] == 200:
            print('Created Bucket '+ sys.argv[2]  + ' in region:', sys.argv[1])
            # subprocess.Popen(export S3BUCKETNAME=sys.argv[2])
            os.putenv('S3BUCKETURL', str(newbucket['ResponseMetadata']['HTTPHeaders']['location']))
            os.environ['S3BUCKETNAME'] = sys.argv[2]
    else:
        print('Bucket Already Exists')
except ClientError as error:
        print(error.response)
    #print (newbuckets)
    