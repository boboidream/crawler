#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import argparse
from deal_img import dealImg

# get argument
parser = argparse.ArgumentParser()
parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.0.1')
parser.add_argument('-f', '--begin', help="begin in which one?")
parser.add_argument('-t', '--end', help="end with which one?")
parser.add_argument('-s', action='store_true', dest='small', default=False, help="for phone")
params = parser.parse_args()


rootPath = 'boshanxiaoxu01'
outputPath = 'output'
beginNum = int(params.begin) if params.begin else 1 # 1 first one
endNum = int(params.end) if params.end else None # -1 last one
list = []

# 将 html 转为 pdf
def toPdf(inPath, outPath):
    cmd = 'wkhtmltopdf -s A5 -L 0 -R 0 -T 0 -B 0 "%s" "%s"' % (inPath, outPath)
    
    if params.small:
        print('-----------for phone----------')
        cmd = 'wkhtmltopdf --page-height 133 --page-width 75 -L 0 -R 0 -T 0 -B 0 "%s" "%s"' % (inPath, outPath)
    # subprocess.Popen(cmd, shell=True)
    os.popen(cmd).readlines()
    print('\x1b[6;30;42m' + '成功读取 ' + inPath.split('/')[-1] + '\x1b[0m')
    print('\x1b[6;30;42m' + '成功生成 ' + outPath.split('/')[-1] + '\x1b[0m')

# 创建输出目录
if not os.path.exists(outputPath):
    os.makedirs(outputPath)

# 列表找到文件夹名称
for item in os.listdir(rootPath):
    m = os.path.join(rootPath, item)

    if os.path.isdir(m):
        list.append(item)

# 打开 index.html 处理文本，重命名
list.sort()
re_title = re.compile(r"(?<=<title>).*?(?=</title>)", re.IGNORECASE)
re_date = re.compile(r"(?<=<em\ id=\"post-date\"\ class=\"rich_media_meta\ rich_media_meta_text\">).*?(?=</em>)")

for webFolder in list[beginNum - 1 : endNum]:
    indexPath = os.path.join(rootPath, webFolder, 'index.html')
    newHtml = os.path.join(rootPath, webFolder, webFolder + '.html')

    if os.path.exists(indexPath):
        with open(indexPath) as f:
          content = f.read()

        with open(newHtml, 'w') as f:
          title = re.search(re_title, content)[0] or webFolder
          dateArr = re.search(re_date, content)[0].split('-')
          mouth = ('0' + dateArr[1])[-2:]
          day = ('0' + dateArr[2])[-2:]
          date = "%s-%s-%s" % (dateArr[0], mouth, day)
          # date = re.search(re_date, content)[0]

          imgDic = dealImg(os.path.dirname(indexPath))
          imgDic['NASA中文'] = ''

          pattern = re.compile('|'.join(imgDic.keys()))
          content = pattern.sub(lambda m: imgDic[m.group(0)], content)

          f.write(content)
        
        outPath = os.path.join(outputPath, "%s-%s.pdf" % (date, title))
        toPdf(newHtml, outPath)
    else:
        print('[Notice] No index.html in ' + webFolder)

