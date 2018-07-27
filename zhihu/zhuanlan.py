#! /usr/bin/env python3
# coding: utf-8

cid = 'boshanlu'

#-----------------------------
import os
import re
import time
from urllib.request import urlopen
from zhihu_oauth import ZhihuClient
from zhihu_oauth.exception import NeedCaptchaException


def download(cid):
    client = ZhihuClient()
    client.load_token('token.pk1') # 登陆
    column = client.column(cid)
    images_dir = os.path.join(column.title, 'images')
    regex = re.compile(r"https://pic\d.zhimg.com/", re.IGNORECASE)

    if not os.path.exists(column.title):
        os.makedirs(column.title)

    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

    for index, article in enumerate(column.articles):
        # 处理文章
        article_f = dealArticle(article)

        # 下载图片
        downloadImg(article_f['content'], images_dir)

        # 替换图片路径
        article_f['content'] = re.sub(regex, './images/', article_f['content'])

        # 写入
        with open(os.path.join(column.title, article_f['title']), 'w+') as f:
            f.write(article_f['content'])

        print('[%s] download %s success!' % (str(index), article.title))


def downloadImg(aritcle, images_dir):
    images_array = re.findall(r'(?<=src=")https://pic\d.zhimg.com/.+?\.(?:png|jpg|jpeg)', aritcle)

    for image in images_array:
        try:
            img_data = urlopen(image).read()
            img_name = os.path.join(images_dir, image.split('/')[-1])

            output = open(img_name, 'wb+')
            output.write(img_data)
            output.close()
        except Exception as e:
            print("type error: " + str(e))


def dealArticle(article):
    banner = ''

    if article.image_url:
        banner = '<img src="' + article.image_url + '" width="960">\n'
    title = '<h1>' + article.title + '</h1>'
    st = time.localtime(article.updated_time)
    date = time.strftime('%Y-%m-%d %H:%M:%S', st)
    dateStr = '<p>' + date + ' | ' + article.author.name + '</p>\n'

    title_format = date[0:10] + article.title.replace('/', '|') + '.html'
    article_html = banner + title + dateStr + article.content + '\n'

    return {
        'title': title_format,
        'content': article_html
    }


# 下载专栏
download(cid)
