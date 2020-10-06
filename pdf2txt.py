# import urllib.request
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser, PDFDocument


# import logging
# logging.getLogger().setLevel(logging.ERROR)


def parse(_path):
    fp = open(_path, 'rb')  # rb以二进制读模式打开本地pdf文件
    # request = Request(_path)  # 随机从user_agent列表中抽取一个元素
    # fp = urlopen(request)  # 打开在线PDF文档
    # fp = urllib.request.urlopen(url)
    # html = fp.read()
    # print(html)
    # 用文件对象来创建一个pdf文档分析器
    praser_pdf = PDFParser(fp)

    # 创建一个PDF文档
    doc = PDFDocument()

    # 连接分析器 与文档对象
    praser_pdf.set_document(doc)
    doc.set_parser(praser_pdf)

    # 提供初始化密码doc.initialize("123456")
    # 如果没有密码 就创建一个空的字符串
    doc.initialize()

    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        f = open(_path.replace("pdf", "txt"), 'w', encoding='utf-8')
        # 创建PDf资源管理器 来管理共享资源
        rsrcmgr = PDFResourceManager()

        # 创建一个PDF参数分析器
        laparams = LAParams()

        # 创建聚合器
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)

        # 创建一个PDF页面解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # 循环遍历列表，每次处理一页的内容
        # doc.get_pages() 获取page列表
        for page in doc.get_pages():
            # print(page)
            # 使用页面解释器来读取
            interpreter.process_page(page)

            # 使用聚合器获取内容
            layout = device.get_result()

            # 这里layout是一个LTPage对象,里面存放着这个page解析出的各种对象,一般包括LTTextBox,LTFigure,LTImage,LTTextBoxHorizontal等等想要获取文本就获得对象的text属性，
            for out in layout:
                # 判断是否含有get_text()方法，图片之类的就没有
                # if hasattr(out,"get_text"):
                if isinstance(out, LTTextBoxHorizontal):
                    results = out.get_text()
                    f.write(results)
                    # print("results: " + results)
        f.close()
    fp.close()


if __name__ == '__main__':
    print('test_example: path = 2009.00001.pdf')
    path = '2009.00001.pdf'
    parse(path)
