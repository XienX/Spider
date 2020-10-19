# pdf转txt

import os
import shutil
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.psparser import PSException
import datetime
import logging

logging.getLogger().setLevel(logging.ERROR)


def pdf_to_txt(pdf_num_queue, pdf_file_queue, total, temp_path, txt_path):
    succeed = 0
    failed = 0
    re_download = set()  # 要求重新下载文件集合

    while succeed + failed < total:
        pdf = pdf_file_queue.get()
        if pdf == '*':
            failed += 1
        else:
            try:
                parse(pdf, txt_path)
            except PSException:
                if pdf in re_download:
                    re_download.remove(pdf)
                    print(f'[{pdf} 再次打开失败，放弃]')
                    failed += 1
                else:
                    print(f'[{pdf} 打开失败]')
                    pdf_num_queue.put(pdf[-14:-4])
                    re_download.add(pdf)
            else:
                succeed += 1
                if pdf in re_download:
                    re_download.remove(pdf)

            os.remove(pdf)

        print(datetime.datetime.now().strftime("%y/%m/%d %H:%M") + f' pdf to txt [{succeed}/{total} succeed, {failed}/{total} failed]')

    print(datetime.datetime.now().strftime("%y/%m/%d %H:%M") + f' 完成，共计{total}个下载任务，成功{succeed}个，失败{failed}个')
    shutil.rmtree(temp_path)


def parse(pdf, txt_path):
    fp = open(pdf, 'rb')

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
        f = open(txt_path + pdf[-15:-4] + '.txt', 'w', encoding='utf-8')
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
    print('pdf2txt test')
    pdf_name = r'D:\EnglishSynonymRecommendation\data\2009.00001.pdf'
    path = r'D:\EnglishSynonymRecommendation\data'
    parse(pdf_name, path)
