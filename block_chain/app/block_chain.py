# -*- coding: utf-8 -*-

import os

import tornado.ioloop
import tornado.web
import datetime
import json
from tornado.options import define, options

from util import select_from_db
from util import draw_detail
from util import draw_list
from util import send_email


define("port", default="8888", help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = {
            (r'/blockChain/index', Index),
            (r'/blockChain/title', Title),
            (r'/blockChain/detail', Detail)
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
        result = [[i[0], datetime.datetime.strftime(i[1], '%Y-%m-%d %H:%M:%S'), i[2], i[3], i[4]] for i in db_info]
        self.render("index.html", result=result, num=len(result))

    def post(self):
        ids = self.get_argument("ids")[1:-1].split(",")
        param = ",".join(ids)

        sql = "select date, title, summary from block_chain where id in (%s)" % param
        result = select_from_db(sql)
        draw_list(result)
        file_list = []
        for i in range(0, len(result)):
            draw_detail(result[i], i)
            file_list.append("%s.png" % i)
        file_list.append("list.png")
        try:
            send_email(file_list)
            self.write(json.dumps({'ok': "已经成功发送邮件，请查收"}))
        except Exception as e:
            self.write(json.dumps({'error': "发送邮件失败，请联系开发者"}))


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


def main():
    tornado.options.parse_command_line()
    Application().listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
