import subprocess
import fitz
import ocrmypdf
from app.service.helper.xml_parser import find_rectangle_boxes


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
            # subprocess.Popen(['ocrmypdf', filepath, 'converted.pdf'])
            ocrmypdf.ocr(filepath, "/home/nirav/PycharmProjects/PDF-Annotation/app/static/converted.pdf")
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

            text = ''
            is_electronic = False
            for page in doc:
                text += page.get_text()
                if len(set([i for i in text if i.isalpha()])) > 1:
                    is_electronic = True
                    break
            if is_electronic:
                self.data[file.split('/')[-1]] = self.extract_data(doc, rect_boxes)
            else:
                self.covert_vectored_to_electronic(file)
                converted_doc = fitz.open("/home/nirav/PycharmProjects/PDF-Annotation/app/static/converted.pdf")
                self.data[file.split('/')[-1]] = self.extract_data(converted_doc, rect_boxes)

        return self.data
