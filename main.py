# 爬虫部分（测试）
# XieXin
# 2020/10
# https://arxiv.org/
# https://arxiv.org/multi?group=grp_cs&%2Fform=Form+Interface
# https://arxiv.org/list/cs/2009?skip=0&show=25
# https://arxiv.org/pdf/2009.00001.pdf
import urllib.request
import urllib.error
import re

import pdfminer.pdfparser

import spider
import pdf2txt

if __name__ == '__main__':
    response = urllib.request.urlopen('https://arxiv.org/list/cs/2009?skip=50&show=25', timeout=30)
    html = response.read().decode('utf-8')
    reStr = re.compile(r'/pdf/\d*\.\d*')
    datalist = re.findall(reStr, html)  # 匹配此页上所有pdf地址

    # with open('list.txt', 'w', encoding='utf-8') as fp:
    #     for data in datalist:
    #         fp.write(data + '\n')

    for data in datalist:  # data格式：/pdf/2009.00110
        try:
            file_path = spider.get_pdf(data)
            pdf2txt.parse(file_path)
        except urllib.error.URLError as e:  # 链接打开异常处理
            print('failed to download ' + data)
            if hasattr(e, "code"):  # 判断是否有状态码
                print(e.code)  # 状态码
            if hasattr(e, "reason"):  # 判断是否有异常原因
                print(e.reason)  # 异常原因
        except pdfminer.pdfparser.PDFException:  # 2
            html_str = 'OtherError'
