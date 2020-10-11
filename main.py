#  -*- coding: UTF-8 -*
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
import spider
import pdf2txt
import datetime
import queue
from concurrent.futures import ThreadPoolExecutor
import os
import shutil
import random

filePath = r'D:\EnglishSynonymRecommendation\data'  # 在此配置文件放置位置
# dataProcessPath = r'D:\EnglishSynonymRecommendation\EngLishLearner\DataProcessing\target\classes\com\xidian\run\Run'  # 在此配置数据处理程序位置
config_file = 'config.txt'
pdf_num_queue = queue.Queue()
pdf_path_queue = queue.Queue()
year_month = ''
last_pdf_file = ''
total = 0


def get_all():  # 获取此月CS总论文数
    req = urllib.request.Request(url='https://arxiv.org/list/cs/' + year_month,
                                 headers={'User-Agent': random.choice(spider.user_agent)})
    response = urllib.request.urlopen(req, timeout=30)
    html = response.read().decode('utf-8')
    re_str = re.compile(r'total of \d* entries')
    result = re.search(re_str, html)  # 匹配此页上所有pdf地址
    return int(result.group().split()[2])


def add_pdf(skip):  # 根据传入的skip，将此页的pdf编号放入pdf_num_queue
    global total
    # response = urllib.request.urlopen('https://arxiv.org/list/cs/2009?skip=50&show=25', timeout=30)
    req = urllib.request.Request(url='https://arxiv.org/list/cs/' + year_month + '?skip=' + str(skip) + '&show=25',
                                 headers={'User-Agent': random.choice(spider.user_agent)})
    response = urllib.request.urlopen(req, timeout=30)
    html = response.read().decode('utf-8')
    re_str = re.compile(r'/pdf/\d*\.\d*')
    datalist = re.findall(re_str, html)  # 匹配此页上所有pdf地址
    datalist.reverse()  # 逆序
    for data in datalist:  # data格式：/pdf/2009.00110
        # print("序号：%s   值：%s" % (datalist.index(data), data))
        num = data[5:]
        if num > last_pdf_file:
            pdf_num_queue.put(num)
            total += 1
        else:
            return False
    return True


def main():
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' 爬虫运行...')

    # 检查今日应爬文件的文件夹是否存在
    data_path = filePath + '\\' + datetime.datetime.now().strftime("%y%m%d")
    if os.path.isdir(data_path):  # 文件夹存在，选择删除或退出
        choice = input('今日爬虫的数据存放文件夹已存在，输入d 删除文件夹继续运行爬虫，其他键退出\n')
        if choice == 'd':
            shutil.rmtree(data_path)
        else:
            exit(0)
    os.mkdir(data_path)  # 创建文件夹

    global year_month
    global last_pdf_file

    # 读取配置文件，获取上次结束的pdf文件编号
    config = filePath + '\\000000\\' + config_file
    if os.path.isfile(config) and os.path.getsize(config):  # 配置文件存在且不为空
        with open(config, "r") as f:  # 打开文件
            year_month = f.readline().strip()  # 读取文件
            last_pdf_file = f.readline().strip()  # 上次结束的pdf文件编号
    else:  # 配置文件不存在或为空
        year_month = datetime.datetime.now().strftime("%y%m")
        last_pdf_file = year_month + '.00000'  # 注意：若未配置config文件，第一次启动时会读取当月所有论文，耗时长！！！

    # 获取当前论文总数
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' 获取当前论文总数...')
    all_pdf = get_all()
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + f' 当前论文总数: {all_pdf}')

    # 创建爬虫线程池，运行
    thread_pool = ThreadPoolExecutor(10)  # 创建线程池，进行下载任务
    for i in range(10):
        thread_pool.submit(spider.get_pdf, pdf_num_queue, pdf_path_queue, data_path)

    # 将本次需要爬取的pdf文件加入pdf_num_queue
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' 获取此次所需下载论文链接并下载...')
    all_pdf -= 25
    while add_pdf(all_pdf):
        # print('25')
        all_pdf -= 25
        if all_pdf < 0:
            pass  # 需单独处理，下次完成

    if total == 0:
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' 无更新')
        os.system("pause")
        exit(0)

    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + f' 此次所需下载论文数： {total}')

    # pdf转txt
    max_pdf = pdf2txt.pdf_to_txt(pdf_num_queue, pdf_path_queue, total)

    # 重写配置文件，更新年月和pdf文件编号
    with open(config, "w") as f:
        f.write(year_month + '\n')
        f.write(max_pdf[-14:-4])

    # 调用数据处理程序
    # os.system('java ' + dataProcessPath)

    # thread_pool.shutdown(wait=False)

    os.system("pause")


if __name__ == '__main__':
    main()
