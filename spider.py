import urllib.request


def get_pdf(url):
    file_name = url.split("/")[-1]
    u = urllib.request.urlopen(url)
    f = open(file_name, 'wb')
    print("downloading" + " " + file_name)
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
        f.write(buffer)
    f.close()
    print("Successful to download" + " " + file_name)
    return file_name

    # 向指定的url地址发送请求，并返回服务器响应的类文件对象
    # response = urllib.request.urlopen('https://arxiv.org/list/cs/2009?skip=0&show=25')

    # 服务器返回的类文件对象支持python文件对象的操作方法
    # read()方法就是读取文件里的全部内容，返回字符串
    # html = response.read()
    # print(html)

    # fileObject = open("test.txt", "wb")
    # fileObject.write(html)
    # fileObject.close()


if __name__ == '__main__':
    print('test_example: url = https://arxiv.org/pdf/2009.00001.pdf')
    url = 'https://arxiv.org/pdf/2009.00001.pdf'
    get_pdf(url)
