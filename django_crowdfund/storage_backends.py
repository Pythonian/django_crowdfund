import os
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage, SpooledTemporaryFile
#from django.core.files.storage import get_storage_class


class StaticStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'public-read'


class MediaStorage(S3Boto3Storage):
    location = settings.AWS_MEDIA_LOCATION
    default_acl = 'public-read'
    # user uploaded files wont overwrite existing files
    file_overwrite = False

    def _save_content(self, obj, content, parameters):
        """
        We create a clone of the content file as when this is passed to boto3
        it wrongly closes the file upon upload where as the storage backend 
        expects it to still be open. Fix: http://bit.ly/2YQGz0I
        """
        # Seek our content back to the start
        content.seek(0, os.SEEK_SET)
        # Create a temporary file that will write to disk after a specified size
        content_autoclose = SpooledTemporaryFile()
        # Write our original content into our copy that will be closed by boto3
        content_autoclose.write(content.read())
        # Upload the object which will auto close the content_autoclose instance
        super(MediaStorage, self)._save_content(obj, content_autoclose, parameters)
        # Cleanup if this is fixed upstream our duplicate should always close
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
