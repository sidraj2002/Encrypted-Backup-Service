# Encrypted-Backup-Service
Service to encrypt and backup files to S3

NewFile -> Directory -> Daemon Detect change -> Pull Encryption Key from Secret -> Symmetric encrypt newFile -> Push to S3 -> Delete key

Daemon -> Check env for S3 Bucket name/URL -> create if not exist -> create new secret -> Push key to AWS/ Creat env variable KeyID 

Future Scope:
 - Prefex encrypted objects pushed to S3
 - Dynamo Table: Encryption key -> S3 object relationaship
 - Key rotation
 - Config File to pull KMS ID for secrets encryption, and other variables
 - Add Inode checking using stat ./TestDir (compare Modified time stamp, if changed check for new files)
 Limitations:
 - Export KeyName and S3BUCKETNAME to OS environment variable (need to use subprocess perhaps) (for persistence)
 - Variables currently exported only within scope of the process, process exit = variable disappears
 - Bootstrap script to install dependences like Cryptography