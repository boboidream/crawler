# -*- encoding=utf8 -*-
__author__ = "zhangwenbo"

from airtest.core.api import *

auto_setup(__file__)

# poco("com.tencent.mm:id/kh").click()
# text(id, search=True)

# Tools

def getCopy(dev):
    return dev.shell('am broadcast -a clipper.get')

def getUrl():
    poco('com.tencent.mm:id/jy', desc='更多').click()
    cw = peco('com.tencent.mm:id/cw', text='复制链接')
    cw.wait_for_appearance()
    cw.click()
    link = getCopy(dev)
    return {
        'type': 'view',
        'url': link
    }
    
def getInfo(btn):
    items_old = peco('android.widget.ListView ').children()
    btn.click()
    items = peco('android.widget.ListView ').children()
    
    if poco('android.webkit.WebView').exists():
        print('这是网页')
        return getUrl()
        
    elif peco('com.tencent.mm:id/oa').exists():
        print('这是小程序')
        name = peco('com.tencent.mm:id/oa').attr('text')
        return {
            'type': 'miniprogram',
            'title': name
        }
    elif items.length > items_old.length:
        print('这是 click')
        length = items.length
        items[length - 1].click()
        more = poco('com.tencent.mm:id/jy', desc='更多')
        more.wait_for_appearance()
        return getUrl()
       