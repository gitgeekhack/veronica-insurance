import subprocess
import fitz
import ocrmypdf
import os
from app.service.helper.xml_parser import find_rectangle_boxes
from app.constant import STATIC_FOLDER


class DataPointExtraction:
    def __init__(self):
        self.data = {}
        self.annotations = {}

    def read_annotated_pdf(self, filepath):
        doc = fitz.open(filepath)
        for page_no, page in enumerate(doc):
            self.annotations[page_no] = []
            for annotation in page.annots():
                self.annotations[page_no].append(annotation.rect)

    @staticmethod
    def covert_vectored_to_electronic(filepath):
        try:
            subprocess.run(['ocrmypdf', filepath,
                            os.path.join(STATIC_FOLDER, f'Converted_files/{filepath.split("/")[-1]}')])
        except:
            pass

    @staticmethod
    def extract_data(doc, rect_boxes):
        single_file_data = {}
        for page_no, datapoints in rect_boxes.items():
            for label, bounding_box in datapoints.items():
                try:
                    single_file_data[label] = doc[page_no].get_textbox(bounding_box)
                except:
                    pass

        return single_file_data

    def extract(self, annotation_file, files):
        rect_boxes = find_rectangle_boxes(annotation_file, files[0])

        for file in files:
            doc = fitz.open(file)

            self.data[file.split('/')[-1]] = self.extract_data(doc, rect_boxes)

            values = list(self.data.values())[0]
            if len(set(values.values())) == 1:
                self.covert_vectored_to_electronic(file)
                converted_doc = fitz.open(os.path.join(STATIC_FOLDER,
                                          f'Converted_files/{file.split("/")[-1]}'))
                self.data[file.split('/')[-1]] = self.extract_data(converted_doc, rect_boxes)

        return self.data
