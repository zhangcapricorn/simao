#!/usr/bin/env python
#!encoding=gbk
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
import urllib2

url = "http://huoxun.com/m/lives.html?from=singlemessage&isappinstalled=0"
cookies = {
    'BAIDUID': '7E07F6DA409019A04C7324122309CFD3:FG=1',
    'BDORZ': 'B490B5EBF6F3CD402E515D22BCDA1598',
    'BDRCVFR[feWj1Vr5u3D]': 'I67x6TjHwwYf0',
    'BDUSS': 'FIQ25XdmgzSm1uWWJxazJpc3FSYTFoano0Q3hsbXNsRnFDS1pseTZnUDREb0JhQUFBQUFBJCQAAAAAAAAAAAEAAABE1v5LAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPiBWFr4gVhaYX',
    'BIDUPSID': '7E07F6DA409019A04C7324122309CFD3',
    'HMACCOUNT': '963830DC41A4FDD4',
    'HMVT': '6bcd52f51e9b3dce32bec4a3997715ac|1517985482|8e2a116daf0104a78d601f40a45c75b4|1517983901|',
    'H_PS_PSSID': '22778_1429_21117_17001_22160',
    'Hm_lpvt_f396f0424d21da4c5df398bf0ca78f23': '1517986626',
    'Hm_lvt_f396f0424d21da4c5df398bf0ca78f23': '1517883746,1517985494',
    'MCITY': '-131%3A',
    'PHPSESSID': '58pha01k7ktdqp1aiftgao9g4a',
    'PSINO': '2',
    'PSTM': '1515462505'
}

s = requests.session()
data_get = {'from':'singlemessage', 'isappinstalled':0}
first_request = s.get(url)
data_post = {'cid':'news', 'page':1}
second_post = s.get("http://huoxun.com/cms/api/lives.html?cid=news&page=1", data=data_post)
print second_post.content