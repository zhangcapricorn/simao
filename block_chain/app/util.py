# -*- coding: utf-8 -*-
import datetime
import re
import pymysql
from PIL import Image, ImageFont, ImageDraw
import os
import math
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def modify_date(now, before_time):
    if "小时" in before_time:
        return now - datetime.timedelta(hours=int(re.sub("\D", "", before_time)))
    elif "分钟" in before_time:
        return now - datetime.timedelta(minutes=int(re.sub("\D", "", before_time)))
    elif "昨天" in before_time:
        return now - datetime.timedelta(days=int(re.sub("\D", "", before_time)))
    elif "刚刚" in before_time:
        return now
    else:
        return before_time


def filter_html_tag(str_tag):
    line = str_tag.rstrip()
    pattern = re.compile(r'<([^>]*)>')

    line = pattern.sub('', line)
    line = re.sub('[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）\"]+', "", line)
    return line


def compare_time(publish_time, cmp_time):
    if publish_time == "0000-00-00 00:00:00":
        return False
    if isinstance(publish_time, str):
        if "/" in publish_time:
            temp = publish_time.split(" ")
            y, m, d = [int(i) for i in temp[0].split("/")]
            h, s = [int(i) for i in temp[1].split(":")]
            publish_time = datetime.datetime(y, m, d, h, s)
        else:
            if len(publish_time.split(" ")) == 1:
                publish_time = datetime.datetime.strptime(publish_time, "%Y-%m-%d")
            else:
                publish_time = datetime.datetime.strptime(publish_time, "%Y-%m-%d %H:%M:%S")
    if cmp_time == "":
        return False
    else:
        return (publish_time < cmp_time)


def select_from_db(sql):
    db = pymysql.connect("47.96.4.38", "root", "Xyb909", 'block_chain', use_unicode=True, charset="utf8")
    cursor = db.cursor()
    cursor.execute(sql)
    result = [i for i in cursor.fetchall()]
    db.commit()
    db.close()
    return result


def cut_out_word(word, length):
    t_n = math.ceil(len(word) / length)
    word_list = []
    begin = 0
    end = length
    for n in range(t_n):
        word_list.append(word[begin:end])
        begin = end
        end = begin + length
    return word_list


def draw_list(info):
    back_img = Image.open("../static/img/background.png").convert("RGBA")
    new_img = Image.new("RGBA", back_img.size, (0, 0, 0, 0))
    date_font = ImageFont.truetype(os.path.join("fonts", "msyh.ttf"), 23)
    word_font = ImageFont.truetype(os.path.join("fonts", "msyh.ttf"), 24)
    d = ImageDraw.Draw(new_img)
    the_now = datetime.datetime.strftime(datetime.datetime.now(), "%y-%m-%d")
    d.text((new_img.size[0] - 620, new_img.size[1] - 850),
           the_now + " 最新资讯",
           font=date_font,
           fill="#000000")
    h = 800
    info_num = len(info)
    for i in range(0, info_num):
        tmp = str(i + 1) + ". " + info[i][1]
        word_list = cut_out_word(tmp, 23)
        for word in word_list:
            d.text((new_img.size[0] - 620, new_img.size[1] - h),
                   word,
                   font=word_font,
                   fill="#000000")
            h -= 28
        h -= 30
    out = Image.alpha_composite(back_img, new_img)
    tt = Image.alpha_composite(out, Image.open("../static/img/logo.png").convert("RGBA"))
    # tt.show()
    tt.save("../result/list.png")


def draw_detail(detail, num):
    back_img = Image.open("../static/img/background.png").convert("RGBA")
    new_img = Image.new("RGBA", back_img.size, (0, 0, 0, 0))
    date_font = ImageFont.truetype(os.path.join("fonts", "msyh.ttf"), 23)
    title_font = ImageFont.truetype(os.path.join("fonts", "msyh.ttf"), 25)
    d = ImageDraw.Draw(new_img)
    the_now = datetime.datetime.strftime(datetime.datetime.now(), "%y-%m-%d")
    d.text((new_img.size[0] - 620, new_img.size[1] - 850),
           the_now + "                                            专题咨讯",
           font=date_font,
           fill="#000000")
    h = 800
    title_list = cut_out_word("【" + detail[1] + "】", 23)
    for title in title_list:
        d.text((new_img.size[0] - 620, new_img.size[1] - h),
               title,
               font=title_font,
               fill="#000000")
        h -= 28
    h -= 15
    d_list = cut_out_word(detail[2], 23)
    for de in d_list:
        d.text((new_img.size[0] - 620, new_img.size[1] - h),
               de,
               font=title_font,
               fill="#000000")
        h -= 28

    out = Image.alpha_composite(back_img, new_img)
    tt = Image.alpha_composite(out, Image.open("../static/img/logo.png").convert("RGBA"))
    # tt.show()
    tt.save("../result/%s.png" % num)


def send_email(file_list):
    sender = 'liudiyuhan1@163.com'
    password = '851102ldyh*'
    receivers = ';'.join(["liudiyuhan@dangdang.com"])
    msg = MIMEMultipart()
    msg['Subject'] = '图片'
    msg['From'] = sender
    msg['To'] = receivers

    for file in file_list:
        jpgpart = MIMEApplication(open("../result/%s" % file, 'rb').read())
        jpgpart.add_header('Content-Disposition', 'attachment', filename=file)
        msg.attach(jpgpart)

    client = smtplib.SMTP()
    client.connect('smtp.163.com')
    client.login(sender, password)
    client.sendmail(sender, receivers, msg.as_string())
    client.quit()
