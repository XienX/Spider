# 处理实际网页
import urllib.request
import random
import re
from retrying import retry
import os
import datetime
import socket
socket.setdefaulttimeout(0)

urlHead = 'https://arxiv.org/pdf/'
user_agent = ['Mozilla/5.0 (Windows NT 10.0; WOW64)', 'Mozilla/5.0 (Windows NT 6.3; WOW64)',
              'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
              'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
              'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
              'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
              'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
              'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
              'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
              'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
              'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
              'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
              'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
              'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
              'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
              'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
              'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
              'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
              'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
              'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11']


# 两次retry之间等待1到5秒，重试5次
@retry(stop_max_attempt_number=5, wait_random_min=1000, wait_random_max=5000)
def get_all(year_month):  # 获取此月CS总论文数
    # print(year_month)
    req = urllib.request.Request(url=f'https://arxiv.org/list/cs/{year_month}',
                                 headers={'User-Agent': random.choice(user_agent)})  # 随机从user_agent列表中抽取一个元素
    response = urllib.request.urlopen(req, timeout=30)
    html = response.read().decode('utf-8')
    re_str = re.compile(r'total of \d* entries')
    result = re.search(re_str, html)  # 匹配此页上所有pdf地址
    return int(result.group().split()[2])


# 两次retry之间等待1到5秒，重试5次
@retry(stop_max_attempt_number=5, wait_random_min=1000, wait_random_max=5000)
def add_pdf(pdf_num_queue, year_month, skip):  # 根据传入的skip，将此页的pdf编号放入pdf_num_queue
    # print(f'{year_month} {skip}')
    # response = urllib.request.urlopen('https://arxiv.org/list/cs/2009?skip=50&show=25', timeout=30)
    req = urllib.request.Request(url=f'https://arxiv.org/list/cs/{year_month}?skip={skip}&show=100',
                                 headers={'User-Agent': random.choice(user_agent)})
    response = urllib.request.urlopen(req, timeout=30)
    html = response.read().decode('utf-8')
    re_str = re.compile(r'/pdf/\d*\.\d*')
    datalist = re.findall(re_str, html)  # 匹配此页上所有pdf地址
    for data in datalist:  # data格式：/pdf/2009.00110
        # print("序号：%s  值：%s" % (datalist.index(data), data))
        num = data[5:]
        pdf_num_queue.put(num)
    return len(datalist)


def get_pdf(pdf_num_queue, pdf_file_queue, data_path):  # 下载pdf的线程
    while True:
        pdf_num = pdf_num_queue.get()
        file_name = data_path + '\\' + pdf_num + '.pdf'
        _url = urlHead + pdf_num + '.pdf'
        print(datetime.datetime.now().strftime("%y/%m/%d %H:%M") + " downloading " + file_name)
        try:
            download(file_name, _url)
        except(urllib.error.URLError, OSError) as e:  # 链接打开异常处理
            print(f'[{_url} 网页打开失败]', end=" ")
            print(e)
            pdf_file_queue.put('*')

            try:
                if os.path.exists(file_name):
                    os.remove(file_name)
            except Exception as e:
                print('未知错误', end=" ")
                print(e)
        except Exception as e:
            print('未知错误', end=" ")
            print(e)
        else:
            print(datetime.datetime.now().strftime("%y/%m/%d %H:%M") + " Successful to download " + file_name)
            pdf_file_queue.put(file_name)


# 两次retry之间等待1到5秒，重试3次
@retry(stop_max_attempt_number=3, wait_random_min=1000,wait_random_max=5000)
def download(file_name, _url):  # 根据url下载pdf
    # socket.setdefaulttimeout(10)
    # print(datetime.datetime.now().strftime("%y/%m/%d %H:%M") + ' ' + _url)
    # raise TimeoutError
    req = urllib.request.Request(url=_url, headers={'User-Agent': random.choice(user_agent)})
    # with urllib.request.urlopen(req, timeout=600) as u:
    u = urllib.request.urlopen(req, timeout=60)
    with open(file_name, 'wb') as f:
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
            f.write(buffer)
    u.close()


if __name__ == '__main__':
    print('spider test')
    file_name = r'D:\EnglishSynonymRecommendation\data\2009.00173.pdf'
    _url = 'https://arxiv.org/pdf/2009.00173.pdf'
    download(file_name, _url)