# -*- coding: utf-8 -*-
import pymysql
import datetime
import time
import re
import data
import weibo

from util import compare_time
def do_job(d, cmp_time):
    result = []
    # for i in weibo.user_ids:
    #     temp = weibo.get_weibo(i, d, cmp_time)
    #     result.extend(temp)
    result.extend(data.parser_jinse_blockchain(d, cmp_time))
    result.extend(data.parser_jinse_lives(cmp_time))

    # db = pymysql.connect("10.255.254.208", "root", "dell1950", 'Dictionary', use_unicode=True, charset="utf8")
    # cursor = db.cursor()
    # cursor.execute('SET NAMES utf8;')
    # cursor.execute('SET CHARACTER SET utf8;')
    # cursor.execute('SET character_set_connection=utf8;')
    # sql = "insert into block_chain values (null, %s, %s, %s, %s)"
    # cursor.executemany(sql, result)
    # db.close()


def do_loop():
    cmp_time = ''
    while True:
        d = datetime.datetime.now()
        do_job(d, cmp_time)
        time.sleep(60)
        cmp_time = d
        print(d)


if __name__ == "__main__":
    do_loop()
    # tt = "2018/2/7 18:04"
    # dd = "2018-02-08 20:13:04"
    # print(compare_time(tt, "2018-02-08 21:10:09.782910"))
