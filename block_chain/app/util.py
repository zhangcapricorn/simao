# -*- coding: utf-8 -*-
import datetime
import re


def modify_date(now, before_time):
    if "小时" in before_time:
        return now - datetime.timedelta(hours=int(re.sub("\D", "", before_time)))
    elif "分钟" in before_time:
        return now - datetime.timedelta(minutes=int(re.sub("\D", "", before_time)))
    elif "昨天" in before_time:
        return now - datetime.timedelta(days=int(re.sub("\D", "", before_time)))
    elif "刚刚" in before_time:
        return now
    else:
        return before_time


def filter_html_tag(str_tag):
    line = str_tag.rstrip()
    pattern = re.compile(r'<([^>]*)>')
    match_list = pattern.findall(line)

    # for i in range(0, len(match_list)):
    #     print "matched:%s" %match_list[i]
    line = pattern.sub('', line)
    line = re.sub('[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）\"]+', "", line)
    return line


def compare_time(publish_time, cmp_time):
    if publish_time == "0000-00-00 00:00:00":
        return False
    if isinstance(publish_time, str):
        if "/" in publish_time:
            temp = publish_time.split(" ")
            y, m, d = [int(i) for i in temp[0].split("/")]
            h, s = [int(i) for i in temp[1].split(":")]
            publish_time = datetime.datetime(y, m, d, h, s)
        else:
            publish_time = datetime.datetime.strptime(publish_time, "%Y-%m-%d %H:%M:%S")
    if cmp_time == "":
        return False
    else:
        return (publish_time < cmp_time)