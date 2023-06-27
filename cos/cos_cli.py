# -*- coding: utf-8 -*-
from common.logger import logger
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from qcloud_cos.cos_exception import CosClientError, CosServiceError
from cos.config import Config


def create_client(key_id, key_secret):
    try:
        config = CosConfig(Region=Config.REGION, SecretId=key_id, SecretKey=key_secret, Token=Config.TOKEN,
                           Scheme=Config.SCHEME)
        client = CosS3Client(config)
        return client
    except CosClientError or CosServiceError as err:
        logger.error(err)
        return None


def upload_file(local_file_path, cos_file_path):
    client = create_client(Config.SECRET_ID, Config.SECRET_KEY)
    try:
        client.upload_file(
            Bucket=Config.BUCKET,
            Key=cos_file_path,
            LocalFilePath=local_file_path,
            EnableMD5=False,
            progress_callback=None
        )
    except CosServiceError as err:
        logger.error(err)
        raise SystemExit(1)


def get_object_url(cos_file_path):
    client = create_client(Config.SECRET_ID, Config.SECRET_KEY)
    # 判断 COS 上文件是否存在
    try:
        exists = client.head_object(
            Bucket=Config.BUCKET,
            Key=cos_file_path
        )
        if exists:
            url = client.get_object_url(
                Bucket=Config.BUCKET,
                Key=cos_file_path
            )
            return url
    except CosServiceError as err:
        logger.info(err)
        return None
