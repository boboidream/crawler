# 使用说明

依赖 zhihu_oauth

## 登陆
在 login.py 填入自己的用户名和密码
```bash
python3 login.py
```

成功生成 token.pk1 则完成

## 抓某人回答
在 people.py 填入要抓取用户 ID 号。
（访问其知乎主页:`https://www.zhihu.com/people/xxxxxxx/activities` xxxxxxx 部分即是 ID）

```bash
python3 people.py
```

## 抓专栏
zhuanlan.py 填入要抓专栏 ID 号。

```bash
python3 zhuanlan.py
```
