import os
import sys
import json
import unittest

sys.path.insert(0, '.')


try:
    from modules.storage import get_storage_instance
except:
    raise


class StorageTest(unittest.TestCase):
    def setUp(self):
        with open('s3_secret.json', 'r') as src:
            self.s3 = get_storage_instance(
                json.load(src)
            )

    def tearDown(self):
        pass

    def test_list(self):
        data = self.s3.list()
        assert type(data) == list

    def test_upload_list_download_delete(self):
        self.s3.uploadData('test', 'test.txt')
        content = self.s3.downloadData('test.txt')
        assert content == 'test'

        files = self.s3.list()
        assert len(files) == 1 and files[0] == 'test.txt'

        self.s3.deleteData('test', 'test.txt')
        files = self.s3.list()
        assert 'test.txt' not in files


if __name__ == '__main__':
    unittest.main(verbosity=2)
