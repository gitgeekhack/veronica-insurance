import os
import aiohttp_jinja2
from aiohttp import web
import json
from app.constant import UPLOAD_FOLDER, DATA_FOLDER, STATIC_FOLDER
from app.common.utils import allowed_file, save_file
from app.service.pdf_extractor.PDFExtractor import DataPointExtraction
from app.service.helper.annotation_file_extractor import extract_annotation_files
import pandas as pd

annotation_data = None


class HomePage(web.View):
    @aiohttp_jinja2.template('index.html')
    async def get(self):
        return {}


class DataExtraction(web.View):
    @aiohttp_jinja2.template('data_extraction.html')
    async def get(self):
        global annotation_data

        extract_annotation_files()

        annotation_data = {}
        for file in os.listdir(os.path.join(STATIC_FOLDER, 'annotations')):
            filename = file.split('.')[0]
            annotation_data[filename] = {}
        return {'annotated': annotation_data}

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

        data_extracted = extractor.extract(STATIC_FOLDER + '/annotations/' + annotation_file + '.xml',
                                           allowed_files_path)

        df = pd.DataFrame(data_extracted)
        df = df.T
        df.to_csv(DATA_FOLDER + '/' + annotation_file + '.csv')

        return {"json_data": json.dumps(data_extracted), 'annotated': annotation_data}
