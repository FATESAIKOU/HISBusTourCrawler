from .aws_s3 import Driver as S3Driver


def get_storage_instance(config):
    if config['type'] == 's3':
        return S3Driver(config)
    else:
        raise NotImplemented(
            f'No such StorageDriver of type "{config["type"]}"')
