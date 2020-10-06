# 爬虫部分（测试）
# XieXin
# 2020/10
# https://arxiv.org/
# https://arxiv.org/multi?group=grp_cs&%2Fform=Form+Interface
# https://arxiv.org/list/cs/2009?skip=0&show=25
# https://arxiv.org/pdf/2009.00001.pdf
import urllib.request
import re
import spider
import pdf2txt

if __name__ == '__main__':
    # urlHead = 'https://arxiv.org'
    # url = 'https://arxiv.org/pdf/2009.00001.pdf'
    response = urllib.request.urlopen('https://arxiv.org/list/cs/2009?skip=25&show=25', timeout=15)
    # html = response.read()
    # print(html)
    html = response.read().decode('utf-8')
    reStr = re.compile(r'/pdf/\d*\.\d*')  # 匹配所有pdf地址
    datalist = re.findall(reStr, html)

    # with open('list.txt', 'w', encoding='utf-8') as fp:
    #     for data in datalist:
    #         fp.write(data + '\n')

    for data in datalist:  # data格式：/pdf/2009.00110
        # url = urlHead + data + '.pdf'
        # print('url:' + url)
        file_path = spider.get_pdf(data)
        pdf2txt.parse(file_path)

    # file_path = spider.get_pdf(url)
    # pdf2txt.parse(file_path)
