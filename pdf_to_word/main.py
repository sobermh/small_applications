"""
@author:mh
Code is far away from bug
"""

from pdf2docx import Converter


def convert_pdf(path):
    # 需要转的pdf文件
    pdf_file_path = path
    file_name = pdf_file_path[0:-4:]
    # print(file_name)
    # # 输出的word文档
    out_file_path = fr'{file_name}.docx'
    # # 进行转换
    new_converter = Converter(pdf_file_path)
    new_converter.convert(out_file_path)
    new_converter.close()


if __name__ == "__main__":
    convert_pdf(r"人工智能学习笔记v1.0(1).pdf")
