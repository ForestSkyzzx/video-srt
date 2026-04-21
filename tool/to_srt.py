# -*- coding: utf-8 -*-
import traceback
from common.logger import logger
from tool.time_format import ms_to_hours


def make_srt(srt_txt, file_name):
    """将 SRT 文本写入文件"""
    try:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(srt_txt)
    except Exception:
        logger.error(traceback.format_exc())


def to_srt(result_detail):
    """
    将 ResTextFormat=3 的识别结果转为 SRT 字幕。
    ResTextFormat=3 返回的每条 SentenceDetail 已按标点分段，
    配合 SentenceMaxLength 控制行长，直接遍历即可生成字幕。
    """
    srt_lines = []
    try:
        for i, sentence in enumerate(result_detail, 1):
            start_time = ms_to_hours(sentence["StartMs"])
            end_time = ms_to_hours(sentence["EndMs"])
            text = sentence["FinalSentence"]
            srt_lines.append(f"{i}\n{start_time} --> {end_time}\n{text}\n")
        return "\n".join(srt_lines)
    except Exception:
        logger.error(traceback.format_exc())
        return ""
