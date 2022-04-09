''' Generate key and push to AWS secrets manager and export environment variables'''
import boto3
import sys
import os
import subprocess
import cryptography
from botocore.exceptions import ClientError

