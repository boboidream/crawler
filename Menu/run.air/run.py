# -*- encoding=utf8 -*-
__author__ = "zhangwenbo"

from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
import pymongo
import sys
import io
import time
import logging

# 计时开始
start = time.time()
num = 0

# 创建Logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
# 终端Handler
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.INFO)
# 文件Handler
fileHandler = logging.FileHandler('/Users/zhangwenbo/Github/crawler/Menu/log/log.log', mode='w', encoding='UTF-8')
fileHandler.setLevel(logging.NOTSET)
# Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
consoleHandler.setFormatter(formatter)
fileHandler.setFormatter(formatter)
# 添加到Logger中
logger.addHandler(consoleHandler)
logger.addHandler(fileHandler)


# 处理编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

poco = AndroidUiautomationPoco(use_airtest_input=False, screenshot_each_action=False)
dev = device()

def getButton(id):
    def unfollow():
#         back = poco('com.tencent.mm:id/k2', desc='返回')
#         back.click()
        keyevent('BACK')
        btn_unfollow = poco('com.tencent.mm:id/b11', text="不再关注")
        btn_unfollow.click()
        btn_confirm = poco('com.tencent.mm:id/az_')
        btn_confirm.wait_for_appearance()
        btn_confirm.click()
    # 搜索 id
    kh = poco("com.tencent.mm:id/kh")
    kh.set_text(id)
    kh.click()
    dev.yosemite_ime.code("3")

    # 关注
    res = poco('search_result')
    res.wait_for_appearance()
    gzh = poco('android.view.View', text="微信号：" + id)

    if not gzh.exists():
        logger.warning('公众号不存在')
        return False
    gzh.click()

    id_list = poco('android:id/list')
    id_list.wait_for_appearance()

    gzh_name = poco('com.tencent.mm:id/b1q').attr('text')
    btn_follow = poco('android:id/title', text="关注公众号")
    btn_open = poco('com.tencent.mm:id/b10', text="进入公众号")
    if btn_follow.exists():
        btn_follow.click()
    elif btn_open.exists():
        btn_open.click()
    else:
        logger.error('打开公众号出错')

    # 提取菜单
    btn_mes = poco("com.tencent.mm:id/k3")
    btn_mes.wait_for_appearance()
    amx = poco('com.tencent.mm:id/amx')

    if not amx.exists():
        logger.warning('Info: 公众号无菜单')
        unfollow()
        return {'id': id, 'name': gzh_name}

    buttons = []
    frameList = amx.offspring('android.widget.FrameLayout')

    def getName(lists):
        buttons = []
        for node in lists:
            info = {'name': node.attr('text')}
            buttons.append(info)
        return buttons

    for frame in frameList:
        child = frame.children()
        amt = frame.offspring('com.tencent.mm:id/amt')
        info = {'name': amt.attr('text')}
        if child.__len__() > 2:
            amt.click()
            lists = poco('android.widget.TextView')
            time.sleep(0.1)
#             lists.wait_for_appearance()
            info['sub_button'] = getName(lists)
            amt.click()
            time.sleep(0.1)
#             lists.wait_for_disappearance()


        buttons.append(info)

    data = {
        'id': id,
        'name': gzh_name,
        'button': buttons
    }

    # 取消关注
    unfollow()

    return data

# 连接数据库
client = pymongo.MongoClient("mongodb://localhost:27017/")
dblist = client.list_database_names()
db = client["btndb"]
col = db["btn"]

# getid
# infoqchina, xinlang-xinwen, tiny4voice
# id = 'tiny4voice'
with open('/Users/zhangwenbo/Github/crawler/Menu/gid.txt') as f:
    content = f.read().strip().strip(',')

cidarr = content.split(',')

for id in cidarr:
    # 跳过存在数据
    o = col.find_one({'id': id})

    if o != None:
        continue

    # 获取数据
    data = getButton(id)

    if data == False:
        continue

    # 写入数据
    col.remove({'id': id})
    x = col.insert_one(data)

    if x is not None:
        num = num + 1
        log = '[' + str(num) + ']Storage ' + id + ' to db Success! '
    else:
        log = 'Storage '  + id + ' to db Failed.'

    logger.info(log)
    if num > 50:
        break


end = time.time()
logger.info('抓取 ' + str(num) + '条数据，用时：' + end-start)






