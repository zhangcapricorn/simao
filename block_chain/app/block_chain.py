# -*- coding: utf-8 -*-

import os
import pymysql
import tornado.ioloop
import tornado.web
from tornado.options import define, options

define("port", default="8888", help="run on the given port", type=int)
class Application(tornado.web.Application):
    def __init__(self):
        handlers = {
            (r'/blockChain/index', Index),
        }

        pwd = os.getcwd()
        parent_path = os.path.abspath(os.path.dirname(pwd) + os.path.sep + ".")

        settings = dict(
            template_path=os.path.join(parent_path, "templates"),
            static_path=os.path.join(parent_path, "static"),
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class Index(tornado.web.RequestHandler):
    def get(self):
        page = self.get_argument("page")
        end = page * 10
        start = end - 10
        db = pymysql.connect("10.255.254.208", "root", "dell1950", 'Dictionary', use_unicode=True, charset="utf8")
        cursor = db.cursor()
        cursor.execute("select * from block_chain order by date desc limit start, end" % (start, end))
        result = [i for i in cursor.fetchall()]
        db.close()
