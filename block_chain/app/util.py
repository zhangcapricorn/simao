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
import textwrap


def modify_date(now, before_time):
    """格式化时间"""
    if "小时" in before_time:
        return (now - datetime.timedelta(hours=int(re.sub("\D", "", before_time)))).strftime("%Y-%m-%d %H:%M:%S")
    elif "分钟" in before_time:
        return (now - datetime.timedelta(minutes=int(re.sub("\D", "", before_time)))).strftime("%Y-%m-%d %H:%M:%S")
    elif "昨天" in before_time:
        return (now - datetime.timedelta(days=int(re.sub("\D", "", before_time)))).strftime("%Y-%m-%d %H:%M:%S")
    elif "刚刚" in before_time:
        return now
    else:
        return before_time


def filter_html_tag(str_tag):
    """过滤html代码"""
    line = str_tag.rstrip()
    pattern = re.compile(r'<([^>]*)>')

    line = pattern.sub('', line)
    # line = re.sub('[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）\"]+', "", line)
    return line


def compare_time(publish_time, cmp_time):
    """比较出版时间是否小于目标时间，如果小不进行爬取"""
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
    """数据库取值"""
    db = pymysql.connect("47.96.4.38", "root", "Xyb909", 'block_chain', use_unicode=True, charset="utf8")
    cursor = db.cursor()
    cursor.execute(sql)
    result = [i for i in cursor.fetchall()]
    db.commit()
    db.close()
    return result


def get_word_num(word):
    num = 0
    for i in word:
        if i >= u'\u4e00' and i <= u'\u9fa5':
            num += 2
        else:
            num += 1
    return num


def cut_out_word(word, length):
    """根据中英文拼接字符串"""
    result = []
    num = 0
    sum_num = 0
    temp = ""
    w_n = get_word_num(word)
    if w_n <= length:
        result.append(word)
    else:
        for i in word:
            if i >= u'\u4e00' and i <= u'\u9fa5':
                num += 2
                sum_num += 2
            else:
                num += 1
                sum_num += 1

            if num >= length:
                num = 0
                result.append(temp)
                temp = i
            else:
                temp = temp + i
        if temp != "":
            result.append(temp)
    return result


def draw_list(info, time_stmp):
    """画清单图片"""
    back_img = Image.open("../static/img/background.png").convert("RGBA")
    new_img = Image.new("RGBA", back_img.size, (0, 0, 0, 0))
    date_font = ImageFont.truetype(os.path.join("/usr/share/fonts", "msyh.ttf"), 23)
    word_font = ImageFont.truetype(os.path.join("/usr/share/fonts", "msyh.ttf"), 24)
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
        # t_w = textwrap.wrap(tmp, width=27)
        # for t in t_w:
        #     d.text((new_img.size[0] - 620, new_img.size[1] - h), t, font=word_font, fill="#000000")
        #     h -= 26
        word_list = cut_out_word(tmp, 45)
        for word in word_list:
            d.text((new_img.size[0] - 620, new_img.size[1] - h),
                   word,
                   font=word_font,
                   fill="#000000")
            h -= 26
        h -= 25
    out = Image.alpha_composite(back_img, new_img)
    tt = Image.alpha_composite(out, Image.open("../static/img/logo.png").convert("RGBA"))
    # tt.show()
    tt.save("/data/web/wwwroot/image/list_%s.png" % time_stmp)


def draw_detail(detail, num, time_stmp):
    """画详情图片"""
    back_img = Image.open("../static/img/background.png").convert("RGBA")
    new_img = Image.new("RGBA", back_img.size, (0, 0, 0, 0))
    date_font = ImageFont.truetype(os.path.join("/usr/share/fonts", "msyh.ttf"), 23)
    title_font = ImageFont.truetype(os.path.join("/usr/share/fonts", "msyh.ttf"), 26)
    word_font = ImageFont.truetype(os.path.join("/usr/share/fonts", "simsun.ttf"), 27)
    d = ImageDraw.Draw(new_img)
    the_now = datetime.datetime.strftime(datetime.datetime.now(), "%y-%m-%d")
    d.text((new_img.size[0] - 620, new_img.size[1] - 850),
           the_now + "                                            专题资讯",
           font=date_font,
           fill="#000000")
    h = 800
    title_list = cut_out_word("【" + detail[1] + "】", 40)
    for title in title_list:
        d.text((new_img.size[0] - 620, new_img.size[1] - h),
               title,
               font=title_font,
               fill="#000000")
        h -= 33
    h -= 35
    d_list = cut_out_word(detail[2], 40)
    for de in d_list:
        d.text((30, new_img.size[1] - h),
               de,
               font=word_font,
               fill="#000000")
        h -= 30

    out = Image.alpha_composite(back_img, new_img)
    tt = Image.alpha_composite(out, Image.open("../static/img/logo.png").convert("RGBA"))
    # tt.show()
    tt.save("/data/web/wwwroot/image/%s_%s.png" % (num, time_stmp))


def send_email(file_list):
    """发送邮件"""
    sender = 'liudiyuhan1@163.com'
    password = '851102ldyh*'
    receivers = ';'.join(["zhangqiannan@dangdang.com", '408621756@qq.com'])
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
    client.starttls()
    client.login(sender, password)
    client.sendmail(sender, receivers, msg.as_string())
    client.quit()

img_dir = "/data/web/wwwroot/image/"


def get_files(time_stmp):
    """获取文件"""
    tmp = str(time_stmp)
    file_list = []
    for root, dirs, files in os.walk(img_dir):
        for file in files:
            if tmp in file:
                file_list.append(file)
    return file_list

def del_files(time_stmp):
    """删除大于1天的文件"""
    for root, dirs, files in os.walk(img_dir):
        if ".png" in files:
            g = re.search(r'\d{10,}', files)
            if len(g) == 1:
                old_stmp = g(0)
                diff = time_stmp - int(old_stmp)
                if diff > 60*60*24:
                    os.remove(os.path.join(dirs, files))
