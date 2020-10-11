# import urllib.request
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser, PDFDocument
import datetime
import logging

logging.getLogger().setLevel(logging.ERROR)


def pdf_to_txt(pdf_num_queue, pdf_path_queue, total):
    succeed = 0
    failed = 0
    re_download = set()  # 要求重新下载文件集合
    max_pdf = ''

    while succeed + failed < total:
        pdf_path = pdf_path_queue.get()
        parse(pdf_path)  # 需要异常处理，下次做
        succeed += 1
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + f' [{succeed}/{total}] {pdf_path} successful to txt')
        if pdf_path > max_pdf:
            max_pdf = pdf_path

    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + f' 处理完成，共计{total}个下载任务，成功{succeed}个')
    return max_pdf


def parse(_path):
    fp = open(_path, 'rb')

    # 用文件对象来创建一个pdf文档分析器
    parser_pdf = PDFParser(fp)

    # 创建一个PDF文档
    doc = PDFDocument()

    # 连接分析器 与文档对象
    parser_pdf.set_document(doc)
    doc.set_parser(parser_pdf)

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
        f.close()
    fp.close()


if __name__ == '__main__':
    print('test_example: path = 2009.00001.pdf')
    path = '2009.00001.pdf'
    parse(path)
