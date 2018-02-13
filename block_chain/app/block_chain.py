# -*- coding: utf-8 -*-

import os

import tornado.ioloop
import tornado.web
import datetime
import json
import time
from tornado.options import define, options

from util import select_from_db
from util import draw_detail_3
from util import del_files
from util import get_files
from util import join_word


define("port", default="8006", help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = {
            (r'/blockChain/index', Index),
            (r'/blockChain/title', Title),
            (r'/blockChain/detail', Detail),
            (r'/blockChain/images', BCImg)
        }

        pwd = os.getcwd()
        parent_path = os.path.abspath(os.path.dirname(pwd) + os.path.sep + ".")

        settings = dict(
            template_path=os.path.join(parent_path, "templates"),
            static_path=os.path.join(parent_path, "static"),
            img_path=os.path.join(parent_path, "img"),
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class Index(tornado.web.RequestHandler):
    def get(self):
        page = int(self.get_argument("page"))
        end = page * 10
        start = end - 10

        sql = "select * from block_chain order by date desc limit %s, %s" % (start, end)
        db_info = select_from_db(sql)
        result = [[i[0], datetime.datetime.strftime(i[1], '%Y-%m-%d-%H:%M:%S'), i[2], i[3], i[4]] for i in db_info]
        self.render("index.html", result=result, num=len(result), file_list="")

    def post(self):
        ids = self.get_argument("ids")[1:-1].split(",")
        param = ",".join(ids)

        sql = "select date, title, summary from block_chain where id in (%s)" % param
        result = select_from_db(sql)
        time_stmp = int(time.time())

        title_str = ""
        for i in range(0, len(result)):
            temp = join_word("%s. " % (i + 1) + result[i][1], 25)
            title_str = title_str + temp + "\n"
            content = join_word("【" + result[i][1] + "】" + result[i][2], 25)
            draw_detail_3(content, "%s" % i, time_stmp)
        draw_detail_3(title_str, "list", time_stmp)

        del_files(time_stmp)
        self.write(json.dumps({'time_stmp': time_stmp}))


class Title(tornado.web.RequestHandler):
    def post(self):
        value = self.get_argument("value")
        id = self.get_argument("id")
        sql = "update block_chain set title='%s' where id=%s" % (value, id)
        select_from_db(sql)
        self.write(json.dumps({'ok': "修改成功"}))


class Detail(tornado.web.RequestHandler):
    def post(self):
        value = self.get_argument("value")
        id = self.get_argument("id")[:-1]
        sql = "update block_chain set summary='%s' where id=%s" % (value, id)
        select_from_db(sql)
        self.write(json.dumps({'ok': "修改成功"}))


class BCImg(tornado.web.RequestHandler):
    def get(self):
        time_stmp = self.get_argument("time_stmp")
        file_list = get_files(time_stmp)
        href = ["http://47.96.4.38:8009/%s" % i for i in file_list]
        self.render("image.html", result=href)


def main():
    tornado.options.parse_command_line()
    Application().listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
