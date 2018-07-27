#! /usr/bin/env python3
# coding: utf-8

uid = 'po-miao-miao-zhu'

#-----------------------------
import os
import re
import time
from urllib.request import urlopen
from zhihu_oauth import ZhihuClient
from zhihu_oauth.exception import NeedCaptchaException


def download(uid):
    client = ZhihuClient()
    client.load_token('token.pk1') # 登陆
    people = client.people(uid)

    for index, answer in enumerate(people.answers):
        # 下载图片
        downloadImg(answer.content)

        # 处理文本
        article = dealArticle(answer)

        # 写入本地
        if not os.path.exists(uid):
            os.makedirs(uid)

        with open(os.path.join(uid, article['title']), 'w+') as f:
            f.write(article['content'])

        print('[%s] download %s success!' % (str(index), answer.question.title))

def dealArticle(answer):
    regex = re.compile(r"https://pic\d.zhimg.com/", re.IGNORECASE)

    title = '<h1>' + answer.question.title + '</h1>'
    st = time.localtime(answer.updated_time)
    date = time.strftime('%Y-%m-%d %H:%M:%S', st)
    dateStr = '<p>' + date + ' | ' + answer.author.name + '</p>\n\n'
    title_format = date[0:10] + answer.question.title.replace('/', '|') + '.html'

    article = title + dateStr + answer.content + '\n'
    article = re.sub(regex, './images/', article)

    return {
        'title': title_format,
        'content': article
    }


def downloadImg(aritcle):
    images_array = re.findall(r'(?<=src=")https://pic\d.zhimg.com/.+?\.(?:png|jpg|jpeg)', aritcle)
    images_dir = os.path.join(uid, 'images')

    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

    for image in images_array:
        try:
            img_data = urlopen(image).read()
            img_name = os.path.join(images_dir, image.split('/')[-1])

            output = open(img_name, 'wb+')
            output.write(img_data)
            output.close()
        except Exception as e:
            print("type error: " + str(e))

# 下载专栏
download(uid)
