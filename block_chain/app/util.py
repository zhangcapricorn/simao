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
    if type(publish_time) == "str":
        if "/" in publish_time:
            publish_time = publish_time.replace("/", "-")
        try:
            publish_time = datetime.datetime.strptime(publish_time, "%Y-%m-%d %H:%M:%S.%f")
        except Exception:
            publish_time = datetime.datetime.strptime(publish_time, "%Y-%m-%d %H:%M")
    print(publish_time, type(publish_time))
    print(cmp_time, type(cmp_time))
    if cmp_time == "":
        return False
    else:
        return (publish_time < cmp_time)