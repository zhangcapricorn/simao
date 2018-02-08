# -*- coding: utf-8 -*-

import urllib.request
import json


proxy_addr="122.241.72.191:808" #设置代理IP


def use_proxy(url, proxy_addr):
    """定义页面打开函数"""
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")
    proxy = urllib.request.ProxyHandler({'http': proxy_addr})
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    data = urllib.request.urlopen(req).read().decode('utf-8', 'ignore')
    return data


def get_container_id(url):
    """获取微博主页的containerid，爬取微博内容时需要此id"""
    data = use_proxy(url, proxy_addr)
    content = json.loads(data).get('data')
    for data in content.get('tabsInfo').get('tabs'):
        if data.get('tab_type') == 'weibo':
            container_id = data.get('containerid')
    return container_id


def get_weibo(id, file):
    """获取微博内容信息,并保存到文本中，内容包括：每条微博的内容、微博详情页面地址、点赞数、评论数、转发数等"""
    i = 1
    while True:
        url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value='+id
        weibo_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + \
                    id + '&containerid=' + get_container_id(url) + '&page=' + str(i)
        try:
            data = use_proxy(weibo_url, proxy_addr)
            content = json.loads(data).get('data')
            cards = content.get('cards')
            if len(cards) > 0:
                for j in range(len(cards)):
                    # print("-----正在爬取第"+str(i)+"页，第"+str(j)+"条微博------")
                    card_type = cards[j].get('card_type')
                    if card_type == 9 :
                        mblog = cards[j].get('mblog')
                        attitudes_count = mblog.get('attitudes_count')
                        comments_count = mblog.get('comments_count')
                        created_at = mblog.get('created_at')
                        reposts_count = mblog.get('reposts_count')
                        scheme = cards[j].get('scheme')
                        text = mblog.get('text')
                        with open(file, 'a', encoding='utf-8') as fh:
                            fh.write("----第"+str(i)+"页，第"+str(j)+"条微博----"+"\n")
                            fh.write("微博地址："+str(scheme)+"\n"+"发布时间："+str(created_at)+"\n"+"微博内容："+text+"\n"+"点赞数："+str(attitudes_count)+"\n"+"评论数："+str(comments_count)+"\n"+"转发数："+str(reposts_count)+"\n")
                i += 1
            else:
                break
        except Exception as e:
            print(e)
            pass


if __name__ == "__main__":
    user_id = ["6448871601", "1871808700", '3495498135']