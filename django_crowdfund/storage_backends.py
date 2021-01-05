from storages.backends.s3boto3 import S3Boto3Storage, SpooledTemporaryFile
from django.conf import settings
import os
#from django.core.files.storage import get_storage_class


class StaticStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'public-read'


class MediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False

    def _save_content(self, obj, content, parameters):
        content.seek(0, os.SEEK_SET)
        content_autoclose = SpooledTemporaryFile()
        content_autoclose.write(content.read())
        super(MediaStorage, self)._save_content(obj, content_autoclose, parameters)
        if not content_autoclose.closed:
            content_autoclose.close()



# class CachedS3Boto3Storage(S3Boto3Storage):
#     """
#     S3 storage backend that saves the files locally, too.
#     """
#     def __init__(self, *args, **kwargs):
#         super(CachedS3Boto3Storage, self).__init__(*args, **kwargs)
#         self.local_storage = get_storage_class(
#             "compressor.storage.CompressorFileStorage")()

#     def save(self, name, content):
#         self.local_storage._save(name, content)
#         super(CachedS3Boto3Storage, self).save(name, self.local_storage._open(name))
#         return name
