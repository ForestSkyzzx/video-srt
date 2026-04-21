# -*- encoding: utf-8 -*-
import os
import sys

from common.logger import logger
from cos.cos_cli import upload_file, get_object_url
from ffmpeg.ffmpeg import extract_audio
from tencent.config import Config as tencent_config
from common.config import Config
from tencent.tencent_cli import new_audio_file
from tool.to_srt import to_srt, make_srt

# 录音文件识别直接支持的格式（含视频格式）
SUPPORTED_FORMATS = {'.wav', '.mp3', '.m4a', '.flv', '.mp4', '.wma', '.3gp', '.amr', '.aac', '.ogg', '.flac'}


def get_file_ext(path):
    """获取文件扩展名（小写，含点号）"""
    return os.path.splitext(path)[1].lower()


def main():
    if len(sys.argv) < 2:
        logger.info("usage: python main.py <video_or_audio_path>")
        sys.exit(0)

    input_path = sys.argv[1]
    file_ext = get_file_ext(input_path)
    base_name = os.path.splitext(os.path.basename(input_path))[0]

    # 判断格式是否直接支持
    if file_ext in SUPPORTED_FORMATS:
        # 直接支持，无需 ffmpeg 转换
        logger.info(f"format {file_ext} is supported, skip ffmpeg conversion")
        cos_file_path = os.path.basename(input_path)
        upload_file(input_path, cos_file_path)
    else:
        # 不支持的格式，用 ffmpeg 转为 wav
        logger.info(f"format {file_ext} is not supported, converting to wav via ffmpeg")
        audio_path = os.path.join(Config.OUTPUT_PATH, base_name + ".wav")
        extract_audio(input_path, audio_path)
        cos_file_path = os.path.basename(audio_path)
        upload_file(audio_path, cos_file_path)

    # 获取 COS URL
    audio_cos_url = get_object_url(cos_file_path)
    if not audio_cos_url:
        logger.error("failed to get cos url")
        return

    # 创建识别任务并获取结果
    result = new_audio_file(tencent_config.ENGINE_TYPE, audio_cos_url)
    if not result:
        logger.error("recognition result is empty")
        return

    # 生成 SRT 字幕
    srt_txt = to_srt(result)
    if not srt_txt:
        logger.error("failed to generate srt")
        return

    srt_path = os.path.join(Config.OUTPUT_PATH, base_name + ".srt")
    make_srt(srt_txt, srt_path)
    logger.info(f"subtitle file generated: {srt_path}")


if __name__ == "__main__":
    main()
