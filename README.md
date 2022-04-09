# Encrypted-Backup-Service
Service to encrypt and backup files to S3

NewFile -> Directory -> Daemon Detect change -> Pull Encryption Key from Secret -> Symmetric encrypt newFile -> Push to S3 -> Delete key

Daemon -> Check env for S3 Bucket name/URL -> create if not exist -> create new secret -> Push key to AWS/ Creat env variable KeyID 

Future Scope:
 - Prefex encrypted objects pushed to S3
 - Dynamo Table: Encryption key -> S3 object relationaship
 - Key rotation