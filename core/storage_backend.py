from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    location = 'category'
    file_overwrite = False

class PublicMediaStorage(S3Boto3Storage):
    location = 'product'
    file_overwrite = False