
# coding=utf-8
import os
import re
import time
import logging
import pdfkit
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfFileMerger
 
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
{content}
</body>
</html>
"""
 
headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
        'Cookie': '_ga=GA1.2.413374848.1534487957; customerId=5b766e1be16fb9456a38377a; customerToken=938b61b0-a1e8-11e8-aeb1-374a1fc4569b; customerMail=; isLogin=yes; _gid=GA1.2.1635156787.1535334600; aliyungf_tc=AQAAAOfIDUTBDgMAxuURt/vbhh3tllhj; connect.sid=s%3A3h41FNarlGbWqCQphQDp8QoiswyXgePl.1PFioyfK9OZkWGWo%2FhhQDcCkfMb7w%2FtYubKBfP%2FIco0; Hm_lvt_5667c6d502e51ebd8bd9e9be6790fb5d=1534843465,1535077164,1535334591,1535508144; SERVER_ID=5aa5eb5e-f0eda04d; _gat=1; Hm_lpvt_5667c6d502e51ebd8bd9e9be6790fb5d=1535556849'
    }
 
def parse_url_to_html(url, name):
    """
    解析URL，返回HTML内容
    :param url:解析的url
    :param name: 保存的html文件名
    :return: html
    """
    try:
	print("url is", url)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        # 正文
        body = soup.find_all(class_="mazi-article-content dont-break-out")[0]
        # 标题
        title = soup.find(class_="no-mathjax topicTitle").string
 
        # 标题加入到正文的最前面，居中显示
        center_tag = soup.new_tag("center")
        title_tag = soup.new_tag('h1')
        title_tag.string = title
        center_tag.insert(1, title_tag)
        body.insert(1, center_tag)
        html = str(body)
        # body中的img标签的src相对路径的改成绝对路径
        pattern = "(<img .*?src=\")(.*?)(\")"
 
        def func(m):
            if not m.group(3).startswith("http"):
                rtn = m.group(1) + m.group(2) + m.group(3)
                return rtn
            else:
                return m.group(1)+m.group(2)+m.group(3)
        html = re.compile(pattern).sub(func, html)
        html = html_template.format(content=html)
        #html = html.encode("utf-8")
        with open(name, 'wb') as f:
            f.write(html)
        return name
 
    except Exception as e:
 
        logging.error("解析错误", exc_info=True)
 
 
def get_url_list():
    """
    获取所有URL目录列表
    :return:
    """
    urls = []
    url = u"https://gitbook.cn/gitchat/column/59f5daa149cd4330613605ba/topic/59f5e21449cd433061360883"
    while True:
        print("once ", url)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        all_a = soup.select('.column_topic_view a')
        
        end = True
        for a in all_a:
            if len(a.select('.next_icon')) > 0:
                urls.append(url)
                url = "https://gitbook.cn" + a['href']
                end = False
                break
            elif len(a.select('.pre_icon')) > 0:
                end = True
        if end:
            urls.append(url)
            break
    print("urls is", urls)
    return urls
 
 
def save_pdf(htmls, file_name):
    """
    把所有html文件保存到pdf文件
    :param htmls:  html文件列表
    :param file_name: pdf文件名
    :return:
    """
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
        'cookie': [
            ('cookie-name1', 'cookie-value1'),
            ('cookie-name2', 'cookie-value2'),
        ],
        'outline-depth': 10,
    }
    print("htmls:filename", htmls, file_name)
    pdfkit.from_file(htmls, file_name, options=options)
 
 
def main():
    start = time.time()
    file_name = u"springboot"
    urls = get_url_list()
    for index, url in enumerate(urls):
        parse_url_to_html(url, str(index+1) + ".html")
    htmls =[]
    pdfs =[]
    for i in range(1,len(urls)+1):
        htmls.append(str(i)+'.html')
        pdfs.append(file_name+str(i)+'.pdf')
 
        save_pdf(str(i)+'.html', file_name+str(i)+'.pdf')
 
        print("trans complete ",str(i),' html')
 
    merger = PdfFileMerger()
    for pdf in pdfs:
       merger.append(open(pdf,'rb'))
       print u"合并完成第"+str(i)+u'个pdf'+pdf
 
    output = open("springboot_all.pdf", "wb")
    merger.write(output)
 
    print u"输出PDF成功！"
 
    for html in htmls:
        os.remove(html)
        print u"删除临时文件"+html
 
    for pdf in pdfs:
        os.remove(pdf)
        print u"删除临时文件"+pdf
 
    total_time = time.time() - start
    print(u"总共耗时：%f 秒" % total_time)
 
 
if __name__ == '__main__':
    main()
