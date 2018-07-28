# 抓取公众号文章，制为 PDF 电子书

## 一、抓取
使用工具抓下文章 html 文件
[f111fei/article_spider](https://github.com/f111fei/article_spider)

## 二、批量转换为 pdf
设置上一步得到的 html 文件夹路径

```python
rootPath = 'root folder'
```

运行
```bash
python3 html2pdf.py
```

可选参数说明：
从第 2 条，转换到 20 条，适合手机大小 pdf（默认适合电脑）
```
python3 html2pdf.py -f 2 -t 20 -s
```

## 三、生成电子书
```python
python3 mergepdf.py
```

最终生成 pdf 电子书于 `prod` 目录。
