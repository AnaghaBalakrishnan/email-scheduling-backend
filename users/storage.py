# users/storage.py
from storages.backends.s3boto3 import S3Boto3Storage

class ProfilePictureStorage(S3Boto3Storage):
    """Custom storage class for profile pictures"""
    location = 'profile_pics'
    file_overwrite = False
