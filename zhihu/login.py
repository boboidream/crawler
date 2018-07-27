#! /usr/bin/env python3
# coding: utf-8

username = 'zhihu username'
pwd = 'zhihu password'

username = '644381492@qq.com'
pwd = '!fGP+GT5dSK*'

#-----------------------------
from zhihu_oauth import ZhihuClient
from zhihu_oauth.exception import NeedCaptchaException

client = ZhihuClient()

try:
    client.login(username, pwd)
except NeedCaptchaException:
    # 保存验证码并提示输入，重新登录
    with open('a.gif', 'wb') as f:
        f.write(client.get_captcha())
    captcha = input('please input captcha:')
    client.login(username, pwd, captcha)

client.save_token('token.pk1') # 保存 token
