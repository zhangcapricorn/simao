# -*- coding: utf-8 -*-
import time
from PIL import Image, ImageFont, ImageDraw
import textwrap
import datetime
import re
import os
from util import draw_detail_3
from util import join_word
from util import select_from_db

if __name__ == "__main__":
    sql = "select date, title, summary from block_chain where id in (%s)" % ('7926')
    result = select_from_db(sql)

    content = join_word("【" + result[0][1] + "】" + result[0][2], 24)
    draw_detail_3(content, "../result/1.png", 1111111111)

    title_str = ""
    for i in range(0, len(result)):
        temp = join_word("%s. " % (i + 1) + result[i][1], 25)
        title_str = title_str + temp + "\n"
    draw_detail_3(title_str, "../result/list.png", 1111111111)


