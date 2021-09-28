import os

import fitz
import datetime
from extract import extract_data

path = "D:/Office/veronica/ITC/files/"
# files = os.listdir(path)
files = ['ITC_Dayline Duran.pdf']
c = 1
import io

import requests


def file_downloader(url):
    r = requests.get(url, allow_redirects=True)
    filename = url.split('/')[-1]
    content = io.BytesIO(r.content)
    return content

# x = file_downloader('http://127.0.0.1:8000/Alliance%20example%206%20Receipt.pdf')
# print(x)

# for filepath in files:
filepath = './files/ITC_Adriana Salgado.pdf'
with fitz.open(filepath) as doc:
    nblocks = []
    for page in doc:
        nblocks.extend(page.getText("dict")['blocks'])

    start_time = datetime.datetime.now()
    data = extract_data(nblocks, filepath)
    end_time = datetime.datetime.now()
    time_diff = (end_time - start_time)
    execution_time = time_diff.total_seconds() * 1000
    print('*' * 100)
    print(f'# {c} Document: [{filepath}] Took: [{execution_time} ms]')
    print('*' * 100)
    for k, v in data.items():
        print(f'{k:<30} => {v}')
    print()
    print()
    c += 1
    # doc.save(f'./out/out_{filepath}.pdf')