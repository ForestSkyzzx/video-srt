# -*- encoding: utf-8 -*-
def time_format(src_time):
    basic_format = "00:00:00,000"
    src_time = src_time.replace(".", ",")
    msel = src_time.split(",")[1]
    hms = src_time.split(",")[0].split(":")
    result = ""
    for i in range(len(hms)):
        if len(hms[i]) < 2:
            hms[i] = "0" + hms[i]
            result += hms[i] + ":"
        else:
            result += hms[i] + ":"
    result = result[:-1]

    if len(result.split(":")) < 3:
        result = "00:" + result
    result = result + "," + msel
    return result


def ms_to_hours(millis):
    seconds = (millis / 1000) % 60
    seconds = int(seconds)
    minutes = (millis / (1000 * 60)) % 60
    minutes = int(minutes)
    hours = (millis / (1000 * 60 * 60)) % 24
    hours = int(hours)
    lay = millis - hours * 1000 * 60 * 60 - minutes * 1000 * 60 - seconds * 1000
    return time_format("%d:%d:%d.%d" % (hours, minutes, seconds, lay))
