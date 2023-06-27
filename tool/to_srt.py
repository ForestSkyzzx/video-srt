# -*- coding: utf-8 -*-
import traceback
from common.logger import logger
from tool.time_format import ms_to_hours
import subprocess


def make_srt(srt_txt, file_name):
    file_name = file_name
    try:
        subprocess.check_call(["touch", file_name], shell=False)
        f = open(file_name, "w")
        f.write(srt_txt)
        f.close()
    except Exception as err:
        logger.error(traceback.format_exc())

def to_srt(src_txt):
    # 设置单行字幕最大字数（也可在创建录音文件识别任务时直接使用SentenceMaxLength参数，免除关于basic_line的处理操作）
    basic_line = 15
    srt_txt = ""
    count = 1
    try:
        for i in range(len(src_txt)):
            current_sentence = src_txt[i]["FinalSentence"]
            last_time = ms_to_hours(src_txt[i]["StartMs"])
            len_rec = len(current_sentence)
            if len_rec > basic_line:
                start_rec = 0
                loc_rec = 0
                start_word = 0
                last_time = ms_to_hours(src_txt[i]["StartMs"])  # 初始为本句开始时间
                while len_rec > basic_line:
                    loc_len = 0
                    loc_offset = 0
                    loc_word = 0

                    for j in range(start_word, src_txt[i]["WordsNum"]):
                        if loc_len + len(src_txt[i]["Words"][j]["Word"]) < basic_line:
                            loc_len += len(src_txt[i]["Words"][j]["Word"])
                            loc_word = j
                            loc_offset = src_txt[i]["Words"][j]["OffsetEndMs"]
                        else:
                            break

                    start_word = loc_word
                    loc_rec = start_rec + loc_len
                    start_time = last_time
                    end_time = ms_to_hours(loc_offset + src_txt[i]["StartMs"])
                    current_txt = current_sentence[start_rec:loc_rec] + "\n"

                    if current_sentence[start_rec:] != "" and current_sentence[start_rec:] != None:
                        srt_txt = srt_txt + str(count) + "\n" + start_time + "-->" + end_time + "\n" + current_txt + "\n"
                        count += 1

                    len_rec = len(current_sentence[loc_rec:])
                    start_rec = loc_rec
                    last_time = end_time

                current_txt = current_sentence[start_rec:] + "\n"
                start_time = last_time
                end_time = ms_to_hours(src_txt[i]["EndMs"])

                if current_sentence[start_rec:] != "" and current_sentence[start_rec:] != None:
                    srt_txt = srt_txt + str(count) + "\n" + start_time + "-->" + end_time + "\n" + current_txt + "\n"
                    count += 1
            else:
                start_time = last_time
                end_time = ms_to_hours(src_txt[i]["EndMs"])
                srt_txt = srt_txt + str(
                    count) + "\n" + start_time + "-->" + end_time + "\n" + current_sentence + "\n" + "\n"
                count += 1
        return srt_txt
    except Exception as err:
        logger.error(traceback.format_exc())
        return ""
