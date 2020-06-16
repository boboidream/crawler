# -*- encoding=utf8 -*-
import pymongo

with open('./gid.txt') as f:
    content = f.read().strip().strip(',')

cidarr = content.split(',')
print(len(cidarr))
# 写入
# 连接数据库
# client = pymongo.MongoClient("mongodb://localhost:27017/")
# dblist = client.list_database_names()
# db = client["btndb"]
# col = db["gid"]

# 清空表
# for gid in cidarr:

