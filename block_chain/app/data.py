# -*- coding: utf-8 -*-
import requests
import re
import json
import datetime
from bs4 import BeautifulSoup

from util import modify_date
from util import filter_html_tag
from util import compare_time


def get_soup(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    return soup


def parser_jinse_blockchain(d, cmp_time):
    url_format = "http://www.jinse.com/blockchain/page_%s"
    result = []
    for i in range(1, 11):
        url = url_format % i
        soup = get_soup(url)
        ol_list = soup.find_all("ol", class_="list clearfix")
        result = []
        try:
            for ol in ol_list:
                publish_time = ol.find_all("li", class_="left")[1].text
                if "·" in publish_time:
                    publish_time = publish_time[3:]

                publish_time = modify_date(d, publish_time)
                if compare_time(publish_time, cmp_time):
                    raise ValueError
                tag_a = ol.find("a")
                title = filter_html_tag(tag_a.get("title"))
                tag_span = ol.find("span", class_="line22 gray8")
                detail = filter_html_tag(tag_span.text)
                if "ZBcom公布HOTC上线计划" in title:
                    print(url_format % i)
                result.append([publish_time, 'jinse-block', title.strip(), detail.strip(), url])
        except ValueError as e:
            break
    return result


def get_publish_date(i, now):
    week_map = {"一": 0, "二": 1, "三": 2, "四": 3, "五": 4, "六": 5, "日": 6}
    publish_time = i["publish_time"]
    if publish_time == None:
        year = now.year
        month = now.month
        day = now.day
        create_time = i["created_at"]
        if "今天" in i["day_name"]:
            publish_time = "%s-%s-%s %s:00" % (year, month, day, create_time)
        elif "昨天" in i["day_name"]:
            yester_day = (now - datetime.timedelta(days=int(1))).day
            publish_time = "%s-%s-%s %s:00" % (year, month, yester_day, create_time)
        elif "前天" in i["day_name"]:
            the_day = (now - datetime.timedelta(days=int(2))).day
            publish_time = "%s-%s-%s %s:00" % (year, month, the_day, create_time)
        else:
            publish_time = "%s-01-01 %s:00" % (year, create_time)
            # week = i["week_name"]
            # p = week_map[week[-1]]
            # n_w = now.weekday()
            # the_day = (now - datetime.timedelta(days=int(n_w - p))).day
            # publish_time = "%s-%s-%s %s:00" % (year, month, the_day, create_time)

    if "·" in publish_time:
        publish_time = publish_time[3:]
    return publish_time


def parser_jinse_lives(cmp_time):
    soup = get_soup("http://www.jinse.com/lives")
    li = soup.find("li", attrs={"class": re.compile("clearfix")})
    id = int(li.get("data-id"))
    url_format = "http://www.jinse.com/ajax/lives/getList?search=&id=%s&flag=down"
    result = []
    now = datetime.datetime.now()
    while True:
        url = url_format % (id)
        req = requests.get(url)
        js = json.loads(req.text)
        data = js["data"]
        dk = data.keys()
        if len(dk) == 0:
            break
        try:
            for k in dk:
                for i in data[k]:
                    publish_time = get_publish_date(i, now)

                    if compare_time(publish_time, cmp_time):
                        raise ValueError

                    content = i["content"]
                    d = []
                    if "】" in content:
                        d = content.split("】")
                    elif "。" in content:
                        d = content.split("。")
                    else:
                        d = content.split(" ")

                    if len(d) < 2:
                        result.append([publish_time, "jinse-lives", filter_html_tag(d[0].strip()), '', url])
                    else:
                        result.append([publish_time, "jinse-lives", filter_html_tag(d[0].strip()), filter_html_tag(" ".join(d[1:])), url])

            id = id - 10
            if id <= 10000:
                break
        except ValueError as e:
            break
    return result


if __name__ == "__main__":
    # week = "星期六"
    # week_map = {"一":0, "二":1, "三":2, "四":3, "五":4, "六":5, "日":6}
    # p = week_map[week[-1]]
    # now = datetime.datetime.now()
    # n_w = now.weekday()
    # print()
    # print((now - datetime.timedelta(days=int(n_w - p))).day)
    parser_jinse_lives("")
