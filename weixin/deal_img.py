#!/usr/bin/python3
# coding: utf-8

import os
from os.path import splitext
from PIL import Image

def dealImg(imgDir):
    res = {}
    for s in os.listdir(imgDir):
        if is_img(os.path.splitext(s)[1]):
            r = checkImg(os.path.join(imgDir, s))

            if r:
                res[r[0]] = r[1]

    return res

def is_img(ext):
    ext = ext.lower()
    if ext == '.jpg':
        return True
    elif ext == '.png':
        return True
    elif ext == '.jpeg':
        return True
    elif ext == '.bmp':
        return True
    else:
        return False


def checkImg(oldimg):
    oldroot = splitext(oldimg)[0]
    oldext = splitext(oldimg)[1][1:]
    im = Image.open(oldimg)

    if im.format.lower() != oldext.lower():
        new_name = oldroot + '.' + im.format.lower()
        im.save(new_name)

        old = os.path.basename(oldimg)
        new =  os.path.basename(new_name)
        r = [old, new]

        print('dealImg：将 %s 另存为 %s' % (old, new))
        return r
    else:
        return False
