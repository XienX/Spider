import urllib.request
import random
from retrying import retry
import datetime

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


# 两次retry之间等待1到5秒，重试3次
#@retry(stop_max_attempt_number=3, wait_random_min=1000,wait_random_max=5000)
def get_pdf(pdf_num_queue, pdf_path_queue, data_path):
    while True:
        pdf_num = pdf_num_queue.get()
        file_name = data_path + '\\' + pdf_num + '.pdf'
        _url = urlHead + pdf_num + '.pdf'
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " downloading " + file_name)
        req = urllib.request.Request(url=_url, headers={'User-Agent': random.choice(user_agent)})  # 随机从user_agent列表中抽取一个元素
        u = urllib.request.urlopen(req)

        f = open(file_name, 'wb')
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
            f.write(buffer)
        f.close()
        pdf_path_queue.put(file_name)
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Successful to download " + file_name)


    # _url = urlHead + pdfNum + '.pdf'
    # file_name = _url.split("/")[-1]
    # print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " downloading " + file_name)
    # req = urllib.request.Request(url=_url, headers={'User-Agent': random.choice(user_agent)})  # 随机从user_agent列表中抽取一个元素
    # u = urllib.request.urlopen(req)
    #
    # f = open(file_name, 'wb')
    # block_sz = 8192
    # while True:
    #     buffer = u.read(block_sz)
    #     if not buffer:
    #         break
    #     f.write(buffer)
    # f.close()
    # print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "Successful to download " + file_name)
    # return file_name

    # for data in datalist:  # data格式：/pdf/2009.00110
    #     try:
    #         file_path = spider.get_pdf(data)
    #         pdf2txt.parse(file_path)
    #     except urllib.error.URLError as e:  # 链接打开异常处理
    #         print('failed to download ' + data)
    #         if hasattr(e, "code"):  # 判断是否有状态码
    #             print(e.code)  # 状态码
    #         if hasattr(e, "reason"):  # 判断是否有异常原因
    #             print(e.reason)  # 异常原因
    #     except pdfminer.pdfparser.PDFException:  # 2
    #         html_str = 'OtherError'


if __name__ == '__main__':
    print('test_example: url = https://arxiv.org/pdf/2009.00001.pdf')
    data = '/pdf/2009.00001'
    get_pdf(data)
