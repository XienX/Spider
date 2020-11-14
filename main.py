# 爬虫入口
# XieXin
# 2020/10

# https://arxiv.org/
# https://arxiv.org/multi?group=grp_cs&%2Fform=Form+Interface
# https://arxiv.org/list/cs/2009?skip=0&show=25
# https://arxiv.org/pdf/2009.00001.pdf
# https://export.arxiv.org/pdf/2009.00001.pdf
# https://export.arxiv.org/list/cs/2010

import urllib.request
import urllib.error
import datetime
from dateutil.relativedelta import relativedelta
import queue
from concurrent.futures import ThreadPoolExecutor
import os
import shutil

import spider
import pdf2txt

filePath = r'D:\EnglishSynonymRecommendation\data'  # 在此配置文件放置位置
dataProcessJar = r'D:\EnglishSynonymRecommendation\EngLishLearner\out\artifacts\DataProcessing_jar\DataProcessing.jar'  # 在此配置数据处理程序
thread_num = 100  # 在此配置爬虫线程数


def main():
    print(datetime.datetime.now().strftime("%y/%m/%d %H:%M") + ' 爬虫运行...')

    pdf_num_queue = queue.Queue()
    pdf_file_queue = queue.Queue()
    year_month = ''
    total = 0
    now_year_month = datetime.datetime.now().strftime("%y%m")

    # 读取文件夹，获取上次运行的年月
    dirs = os.listdir(filePath)
    if len(dirs) > 1:
        print('[error]目标目录下存在多个文件夹，请检查')
        os.system("pause")
        exit(0)
    elif len(dirs) == 0:
        print('没有运行记录，默认爬取上月数据')
        last_month = datetime.date.today() - relativedelta(months=+1)
        year_month = datetime.datetime.strftime(last_month, "%y%m")
    else:
        year_month = dirs[0]
        if year_month == now_year_month:  # 检查本月应爬文件的文件夹是否存在
            print('本月已运行过爬虫！')
            os.system("pause")
            exit(0)
        shutil.rmtree(filePath + '\\' + year_month)  # 删除上次运行遗留的文件夹

    # 创建本次txt数据存储文件夹
    txt_path = filePath + '\\' + now_year_month
    os.mkdir(txt_path)

    # 创建pdf数据临时存储文件夹
    temp_path = filePath + '\\0000'
    os.mkdir(temp_path)

    # 创建爬虫线程池，运行
    thread_pool = ThreadPoolExecutor(thread_num)  # 创建线程池，进行下载任务
    for i in range(thread_num):
        thread_pool.submit(spider.get_pdf, pdf_num_queue, pdf_file_queue, temp_path)

    # 获取所有待爬文件
    print(datetime.datetime.now().strftime("%y/%m/%d %H:%M") + ' 获取论文链接...')
    while year_month < now_year_month:
        try:
            all_pdf = spider.get_all(year_month)
        except(urllib.error.URLError, OSError) as e:  # 链接打开异常处理
            print(f'[{year_month} 网页打开失败]', end=" ")
            print(e)
            # if hasattr(e, "code"):  # 判断是否有状态码
            #     print('e.code')
            #     print(e.code)  # 状态码
            # if hasattr(e, "reason"):  # 判断是否有异常原因
            #     print('e.reason')
            #     print(e.reason)  # 异常原因
            all_pdf = 0
        print(datetime.datetime.now().strftime("%y/%m/%d %H:%M") + f' {year_month} 论文数: {all_pdf}')

        # all_pdf = 100  # 测试用
        # 取pdf编号入pdf_num_queue
        num = 0
        while num < all_pdf:
            try:
                total += spider.add_pdf(pdf_num_queue, year_month, num)
            except(urllib.error.URLError, OSError) as e:  # 链接打开异常处理
                print(f'[{year_month}-{num} 网页打开失败]', end=" ")
                print(e)
            # print(total)
            num += 100

        date = datetime.datetime.strptime(year_month, "%y%m").date()
        new_month = date - relativedelta(months=-1)
        year_month = datetime.datetime.strftime(new_month, "%y%m")
    print(datetime.datetime.now().strftime("%y/%m/%d %H:%M") + f' 此次所需下载总论文数： {total}')

    # pdf转txt
    pdf2txt.pdf_to_txt(pdf_num_queue, pdf_file_queue, total, temp_path, txt_path)

    # 调用数据处理程序
    print('\n调用数据处理程序\n')
    os.system('java -jar ' + dataProcessJar)

    os.system("pause")


if __name__ == '__main__':
    main()
