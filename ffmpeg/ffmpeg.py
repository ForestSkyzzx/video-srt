# -*- coding: utf-8 -*-
import subprocess
import traceback

from common.logger import logger


def extract_audio(video_path, audio_path):
    try:
        ret = subprocess.run("ffmpeg -version", shell=True)
        if ret.returncode != 0:
            logger.info("请先安装 ffmpeg 依赖 ，并设置环境变量")
            raise SystemExit(1)
        ret = subprocess.run(["ffmpeg", "-i", video_path, "-vn", "-ar", "16000", audio_path], shell=False)
        if ret.returncode != 0:
            logger.error(ret)
            raise SystemExit(1)
    except Exception as err:
        logger.error(traceback.format_exc())
        raise SystemExit(1)

