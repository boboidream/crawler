#!/usr/bin/env python3
# coding: utf-8

import os, time
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger

inPath = 'output'
outPath = 'prod'

# 获得正确文件名
def getfiles(dirpath):
    a = []
    for s in os.listdir(dirpath):
        if os.path.splitext(s)[1] == '.pdf':
            a.append(s)
    a.sort()
    return a

# 创建输出目录
if not os.path.exists(outPath):
    os.makedirs(outPath)

# 列表找到文件夹名称
list = getfiles(inPath)

merger = PdfFileMerger()
for filename in list:
    with open(os.path.join(inPath, filename), 'rb') as f:
        file_rd = PdfFileReader(f)
        short_filename = os.path.splitext(filename)[0].split('-')[-1]

        if file_rd.isEncrypted == True:
            print('不支持的加密文件：%s'%(filename))
            continue
        
        merger.append(file_rd, bookmark=short_filename, import_bookmarks=False)
        print('合并文件：%s'%(filename))

now = int(time.time())
out_filename=os.path.join(outPath, str(now) + '.pdf')
merger.write(out_filename)
print('合并后的输出文件：%s'%(out_filename))
merger.close()



