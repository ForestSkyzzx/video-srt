# -*- coding: utf-8 -*-
import json
import time
import io
import sys
import traceback
from common.logger import logger

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.asr.v20190614 import asr_client, models

if sys.version_info[0] == 3:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from tencent.config import Config


def new_audio_file(engine_type, audio_url):
    request_id, task_id = create_rec(engine_type, audio_url)
    ret, result = query_rec_task(task_id)
    if ret:
        return result
    return ""


def create_client(key_id, key_secret):
    try:
        cred = credential.Credential(key_id, key_secret)
        http_profile = HttpProfile()
        http_profile.endpoint = "asr.tencentcloudapi.com"
        client_profile = ClientProfile()
        client_profile.httpProfile = http_profile
        client_profile.signMethod = "TC3-HMAC-SHA256"
        client = asr_client.AsrClient(cred, "ap-shanghai", client_profile)
        return client
    except TencentCloudSDKException as err:
        logger.error(err)
        return None


def create_rec(engine_type, file_url):
    client = create_client(Config.SECRET_ID, Config.SECRET_KEY)
    req = models.CreateRecTaskRequest()
    params = {"ChannelNum": 1, "ResTextFormat": 3, "SourceType": 0, "ConvertNumMode": 1}
    req._deserialize(params)
    req.EngineModelType = engine_type
    req.Url = file_url
    try:
        resp = client.CreateRecTask(req)
        logger.info(resp)
        requesid = resp.RequestId
        taskid = resp.Data.TaskId
        return requesid, taskid
    except Exception as err:
        logger.error(traceback.format_exc())
        return None, None


def query_rec_task(taskid):
    client = create_client(Config.SECRET_ID, Config.SECRET_KEY)
    req = models.DescribeTaskStatusRequest()
    params = '{"TaskId":' + str(taskid) + '}'
    req.from_json_string(params)
    result = ""
    while True:
        try:
            resp = client.DescribeTaskStatus(req)
            resp_json = resp.to_json_string()
            logger.info(resp_json)
            resp_obj = json.loads(resp_json)
            if not resp_obj["Data"]:
                return False, ""
            if resp_obj["Data"]["StatusStr"] == "success":
                result = resp_obj["Data"]["ResultDetail"]
                break
            if resp_obj["Data"]["Status"] == 3:
                return False, ""

            time.sleep(1)
        except TencentCloudSDKException as err:
            logger.info(err)
            return False, ""

    return True, result
