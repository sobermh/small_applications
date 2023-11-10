"""
@author:mh
Code is far away from bug
"""
import os

from openpyxl import load_workbook
from openpyxl.workbook import Workbook


def output(context_list):
    if not os.path.exists("results.xlsx"):
        os.makedirs("results.xlsx")
    workbook = load_workbook("results.xlsx")
    worksheet = workbook["Sheet1"]
    worksheet.append(context_list)
    workbook.save("results.xlsx")

# if __name__ == '__main__':
#     output()
