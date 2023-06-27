# -*- encoding: utf-8 -*-
import sys

from common.logger import logger
from cos.cos_cli import upload_file, get_object_url
from ffmpeg.ffmpeg import extract_audio
from tencent.config import Config as tencent_config
from common.config import Config
from tencent.tencent_cli import new_audio_file
from tool.to_srt import to_srt, make_srt


def main():
    if len(sys.argv) < 1:
        logger.info("enter the video path:")
        logger.info("python main.py [video_path]")
        sys.exit(0)
    video_path = sys.argv[1]
    # 提取的录音文件的路径
    audio_path = Config.OUTPUT_PATH + video_path.split("/")[-1].split(".")[0] + ".wav"
    # 提取录音文件
    extract_audio(video_path, audio_path)
    # 录音文件位于cos桶中的位置
    cos_file_path = audio_path.split("/")[-1]
    # 上传录音文件至cos
    upload_file(audio_path, cos_file_path)
    # 获取录音文件的cos url
    audio_cos_url = get_object_url(cos_file_path)
    if audio_cos_url:
        # 创建录音文件识别任务，并获取识别结果
        result = new_audio_file(tencent_config.ENGINE_TYPE, audio_cos_url)
        if result:
            # 将识别结果转换为srt文件的格式
            srt_txt = to_srt(result)
            if srt_txt:
                # 输出srt文件的路径
                file_name = Config.OUTPUT_PATH + video_path.split("/")[-1].split(".")[0] + ".srt"
                # 写入文件
                make_srt(srt_txt, file_name)
            else:
                logger.error("srt txt is none")
        else:
            logger.error("result is none")
    else:
        logger.error("audio cos url is none")
    logger.info("finish generating the srt file!")


if __name__ == "__main__":
    main()
