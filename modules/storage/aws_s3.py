"""
Implement for using aws s3 as a storage
"""

import io
import os
import boto3
from .storage_interface import StorageInterface


class Driver(StorageInterface):
    def __init__(self, config):
        self._bucket = boto3.resource(
            's3',
            aws_access_key_id=config['key'],
            aws_secret_access_key=config['secret']
        ).Bucket(config['bucket_name'])

        self.dir = config['dir']

    def list(self):
        fns = set()
        for o in self._bucket.objects.filter(Prefix=self.dir):
            if len(o.key) > len(self.dir):
                fns.add(o.key[len(self.dir):].split('/')[0])

        return list(fns)

    def downloadData(self, filename):
        content = io.BytesIO()
        self._bucket.download_fileobj(
            os.path.join(self.dir, filename), content)
        content.seek(0)

        return content.read().decode('utf-8')

    def uploadData(self, text, filename):
        content = io.BytesIO(bytes(text, 'utf-8'))
        self._bucket.upload_fileobj(content, os.path.join(self.dir, filename))

    def deleteData(self, *filenames):
        self._bucket.delete_objects(
            Delete={
                'Objects': [{'Key': os.path.join(self.dir, fn)} for fn in filenames]
            }
        )
