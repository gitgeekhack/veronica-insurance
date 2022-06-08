# import fitz
# from tabula import read_pdf
# from tabulate import tabulate
#
# df = read_pdf('/home/nirav/PycharmProjects/underwriting_automation/app/data/temp/example/application/ALLIANCE_APP_Adriana Salgad.pdf')
#
# print(tabulate(df))
import pprint

import camelot
import matplotlib.pyplot as plt

# extract all the tables in the PDF file
tables = camelot.read_pdf(
    "/home/nirav/PycharmProjects/underwriting_automation/app/data/temp/example/application/ALLIANCE_APP_Adriana Salgad.pdf",
    flavor='stream', edge_tol=10, pages='3',
    table_areas=["40, 355, 600, 250"]
)
print(tables)
# camelot.plot(tables[0], kind='contour')
# plt.show()
tables[0].df.to_csv('file1.csv')

