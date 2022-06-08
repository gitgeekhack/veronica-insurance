import aiohttp_jinja2
import cv2
import numpy as np
from aiohttp import web
import json
from app.constant import UPLOAD_FOLDER, MAXIMUM_UPLOAD, DATA_FOLDER
from app.common.utils import allowed_file, save_file
from app.service.pdf_extractor.PDFExtractor import DataPointExtraction
import glob
import pprint
import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


class HomePage(web.View):
    @aiohttp_jinja2.template('index.html')
    async def get(self):
        return {}


class DataExtraction(web.View):
    @aiohttp_jinja2.template('data_extraction.html')
    async def get(self):
        return {}

    @aiohttp_jinja2.template('data_extraction.html')
    async def post(self):
        data = await self.request.post()
        pdf_files = data.getall('input_pdfs')
        annotation_file = data.get('annote')

        extractor = DataPointExtraction()

        allowed_files_path = []
        for file in pdf_files:
            if allowed_file(file.filename):  # checking for allowed file
                save_file(file, filetype='pdf')
                allowed_files_path.append(UPLOAD_FOLDER + '/pdfs/' + file.filename)

        data_extracted = extractor.extract(UPLOAD_FOLDER + '/annotations/' + annotation_file + '.xml',
                                           allowed_files_path)

        df = pd.DataFrame(data_extracted)
        df = df.T
        df.to_csv(DATA_FOLDER + '/' + annotation_file + '.csv')

        return {"json_data": json.dumps(data_extracted)}


class PDFAnnotation(web.View):
    @aiohttp_jinja2.template('pdf_annotation.html')
    async def get(self):
        return {}

    @aiohttp_jinja2.template('pdf_annotation.html')
    async def post(self):
        return {}