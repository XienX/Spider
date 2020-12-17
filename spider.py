# -*- coding: UTF-8 -*-
# 处理实际网页
import urllib.request
import random
import re
from retrying import retry
import os
import queue
import datetime
import socket
import sys
import shutil
from pathlib import Path

import main
import pdf2txt

socket.setdefaulttimeout(10)

urlHead = 'https://export.arxiv.org/'


# 两次retry之间等待5到30秒，重试5次
@retry(stop_max_attempt_number=5, wait_random_min=5000, wait_random_max=30000)
def get_all(year_month):  # 获取此月CS总论文数
    # print(year_month)
    # req = urllib.request.Request(url=f'{urlHead}list/cs/{year_month}',
    #                              headers={'User-Agent': random.choice(user_agent)})  # 随机从user_agent列表中抽取一个元素
    req = urllib.request.Request(url=f'{urlHead}list/cs/{year_month}')
    response = urllib.request.urlopen(req, timeout=10)
    html = response.read().decode('utf-8')
    re_str = re.compile(r'total of \d* entries')
    result = re.search(re_str, html)  # 匹配此页上所有pdf地址
    return int(result.group().split()[2])


# 两次retry之间等待5到30秒，重试5次
@retry(stop_max_attempt_number=5, wait_random_min=5000, wait_random_max=30000)
def add_pdf(pdf_num_queue, year_month, skip):  # 根据传入的skip，将此页的pdf编号放入pdf_num_queue
    # print(f'{year_month} {skip}')
    # response = urllib.request.urlopen('https://arxiv.org/list/cs/2009?skip=50&show=25', timeout=30)
    # req = urllib.request.Request(url=f'{urlHead}list/cs/{year_month}?skip={skip}&show=100',
    #                              headers={'User-Agent': random.choice(user_agent)})
    req = urllib.request.Request(url=f'{urlHead}list/cs/{year_month}?skip={skip}&show=100')
    response = urllib.request.urlopen(req, timeout=10)
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
        file_name = data_path + '/' + pdf_num + '.pdf'
        _url = urlHead + 'pdf/' + pdf_num + '.pdf'
        print(datetime.datetime.now().strftime("%y/%m/%d %H:%M") + " downloading " + pdf_num + '.pdf')
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
            print(datetime.datetime.now().strftime("%y/%m/%d %H:%M") + " Successful to download " + pdf_num + '.pdf')
            pdf_file_queue.put(file_name)


# 两次retry之间等待5到30秒，重试2次
@retry(stop_max_attempt_number=2, wait_random_min=5000,wait_random_max=30000)
def download(file_name, _url):  # 根据url下载pdf
    # print(datetime.datetime.now().strftime("%y/%m/%d %H:%M") + ' ' + _url)
    # req = urllib.request.Request(url=_url, headers={'User-Agent': random.choice(user_agent)})
    req = urllib.request.Request(url=_url)
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


def download_singer_pdf(url): #单独下载任意pdf链接+转txt
    print(datetime.datetime.now().strftime("%y/%m/%d %H:%M") + ' 下载中...')

    temp_path = main.filePath + '/0000'
    txt_path = main.filePath + '/9999'

    # 删除可能遗留的文件夹
    path = Path(temp_path)
    if path.is_dir():
        shutil.rmtree(temp_path)
    path = Path(txt_path)
    if path.is_dir():
        shutil.rmtree(txt_path)

    # 创建文件夹
    os.mkdir(temp_path)
    os.mkdir(txt_path)

    # 下载
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |' # new_title = re.sub(rstr, "_", title)  # 替换为下划线
    if url[-4:] == '.pdf':
        pdf_name = temp_path + '/' + re.sub(rstr, "_", url)
    else:
        pdf_name = temp_path + '/' + re.sub(rstr, "_", url) + '.pdf'

    try:
        download(pdf_name, url)
    except(urllib.error.URLError, OSError) as e:  # 链接打开异常处理
        print(f'[{url} 网页打开失败]', end=" ")
        print(e)
    except Exception as e:
        print('未知错误', end=" ")
        print(e)
    else:
        print(datetime.datetime.now().strftime("%y/%m/%d %H:%M") + " Successful to download ")

        # pdf转txt
        txt_name = txt_path + '/' + re.sub(rstr, "_", url) + '.txt'
        try:
            pdf2txt.parse(pdf_name, txt_name)
        except Exception:  # 转txt异常
            print(f'[{pdf_name} 打开失败]')
        else:  # 转txt成功
            print(datetime.datetime.now().strftime("%y/%m/%d %H:%M") + ' pdf to txt succeed')
            # 调用数据处理程序
            print('\n调用数据处理程序\n')
            os.system('java -jar ' + main.dataProcessJar)

    # 删除文件夹
    if path.is_dir():
        shutil.rmtree(temp_path)
    if path.is_dir():
        shutil.rmtree(txt_path)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('error: 需要一个参数：PDF链接')
        os.system("pause")
        exit(0)

    download_singer_pdf(sys.argv[1])


    # print('spider test')
    # # file_name = r'D:\EnglishSynonymRecommendation\data\2009.00173.pdf'
    # # _url = 'https://arxiv.org/pdf/2009.00173.pdf'
    # # download(file_name, _url)
    #
    # pdf_num_queue = queue.Queue()
    # pdf_file_queue = queue.Queue()
    # data_path = r'D:\EnglishSynonymRecommendation\data\0000'
    # pdf_num_queue.put('2010.00163')
    # get_pdf(pdf_num_queue, pdf_file_queue, data_path)