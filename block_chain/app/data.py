# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup


def get_soup(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    return soup


def parser_jinse_blockchain():
    soup = get_soup("http://www.jinse.com/blockchain")
    ol_list = soup.find_all("ol", class_="list clearfix")
    for ol in ol_list:
        tag_a = ol.find("a")
        title = tag_a.get("title")
        href = tag_a.get("href")
        tag_span = ol.find("span", class_="line22 gray8")
        detail = tag_span.text
        print(href, detail)


def parser_jinse_lives():
    soup = get_soup("http://www.jinse.com/lives")
    div_list = soup.find_all("div", class_="live-info")
    for div in div_list:
        info = div.text
        d = []
        if "】" in info:
            d = info.split("】")
        else:
            d = info.split("。")
        title = d[0][2:]
        detail = d[1]
        print(title, detail)


if __name__ == "__main__":
    parser_jinse_lives()