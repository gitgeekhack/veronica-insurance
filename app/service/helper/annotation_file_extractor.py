import os
import glob
import zipfile
from app.constant import STATIC_FOLDER


def extract_annotation_files():
    for file in glob.glob('/home/nirav/Downloads/PDF_Annotation/*.zip'):
        if file.split("/")[-1].split(".")[0].capitalize() not in os.listdir(os.path.join(STATIC_FOLDER, 'annotations')):
            with zipfile.ZipFile(file, 'r') as zip_file:
                zip_file.extractall(os.path.join(STATIC_FOLDER, 'annotations'))

                os.rename(os.path.join(STATIC_FOLDER, 'annotations/annotations.xml'),
                          os.path.join(STATIC_FOLDER, f'annotations/{file.split("/")[-1].split(".")[0].capitalize()}.xml'))
