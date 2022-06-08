import pprint
import xmltodict
import fitz


def find_rectangle_boxes(annotation_file, sample_file):
    doc = fitz.open(sample_file)

    with open(annotation_file, 'r', encoding='utf-8') as file:
        my_xml = file.read()

    my_dict = xmltodict.parse(my_xml)

    pdf_width = float(doc[0].bound().x1)
    pdf_height = float(doc[0].bound().y1)

    image_width = float(my_dict['annotations']['image'][0]['@width'])
    image_height = float(my_dict['annotations']['image'][0]['@height'])

    width_ratio = pdf_width / image_width
    height_ratio = pdf_height / image_height

    bounding_box_data = {}
    for page_image in my_dict['annotations']['image']:
        try:
            page_no = int(page_image['@id'])
            # print(page_image)
            if page_image['box']:
                bounding_box_data[page_no] = {}
            if not isinstance(page_image['box'], list):
                page_image['box'] = [page_image['box']]
            # print(page_image)
            for box in page_image['box']:
                bounding_box_data[page_no][box['@label']] = \
                    [width_ratio * float(box['@xtl']), height_ratio * float(box['@ytl']),
                     width_ratio * float(box['@xbr']), height_ratio * float(box['@ybr'])]
        except Exception:
            pass

    return bounding_box_data
