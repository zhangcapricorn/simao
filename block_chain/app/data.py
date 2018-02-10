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
        soup = get_soup(url_format % i)
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
                href = tag_a.get("href")
                tag_span = ol.find("span", class_="line22 gray8")
                detail = filter_html_tag(tag_span.text)

                result.append([publish_time, 'jinse', title.strip(), detail.strip()])
        except ValueError as e:
            break
    return result


def parser_jinse_lives(cmp_time):
    soup = get_soup("http://www.jinse.com/lives")
    li = soup.find("li", attrs={"class": re.compile("clearfix")})
    id = int(li.get("data-id"))
    url_format = "http://www.jinse.com/ajax/lives/getList?search=&id=%s&flag=down"
    result = []
    while True:
        req = requests.get(url_format % (id))
        js = json.loads(req.text)
        data = js["data"]
        dk = data.keys()
        if len(dk) == 0:
            break

        try:
            for k in dk:
                for i in data[k]:
                    publish_time = i["publish_time"]
                    if publish_time == None:
                        continue
                    if "·" in publish_time:
                        publish_time = publish_time[3:]

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
                        result.append([publish_time, "jinse", filter_html_tag(d[0].strip()), ''])
                    else:
                        result.append([publish_time, "jinse", filter_html_tag(d[0].strip()), filter_html_tag(" ".join(d[1:]))])
            id = id - 10
            if id <= 10000:
                break
        except ValueError as e:
            break
    return result


if __name__ == "__main__":
    a = '2017-10-18 22:17:46'
    b = '2017-10-19 22:17:40'
    print(b > a)
