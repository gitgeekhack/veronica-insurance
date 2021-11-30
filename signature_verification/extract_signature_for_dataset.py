import os
import re
import fitz

path = './data/ITC/'
ele_sign = './images/Electronics_ITC/'
photo_sign = './images/Photographics_ITC/'
others = './images/others/'

total_images_on_page = 0

def check_date(blocks):
    flag = False
    for ind, block in enumerate(blocks):
        if block['type'] == 1:
            if ind < len(blocks) - 1 and blocks[ind + 1]['type'] == 0:
                text = blocks[ind + 1]['lines'][0]['spans'][0]['text']
                x = re.search("[0-9]{4}-[0-9]{2}-[0-9]{2}", text)
                if x:
                    flag = True
    return flag

for root, dirs, files in os.walk(path, topdown=True):
    for file in files:
        filepath = os.path.join(root, file)
        doc = fitz.open(filepath, filetype='pdf')
        for page in range(len(doc)):
            for img in doc.getPageImageList(page):
                if img[5] == 'DeviceRGB':
                    if img[1]:
                        pix_no = fitz.Pixmap(doc, img[0])
                        mask = fitz.Pixmap(doc, img[1])
                        pix = fitz.Pixmap(pix_no, mask)
                        blocks = doc[page].getText('dict')['blocks']
                        date = check_date(blocks)
                        if date:
                            pix.save(ele_sign + file.split('.')[0] + str(page + 1) + '_'
                                     + str(total_images_on_page) + '.png')
                        else:
                            pix.save(photo_sign + file.split('.')[0] + str(page + 1) + '_'
                                     + str(total_images_on_page) + '.png')
                        total_images_on_page += 1
                    else:
                        xref = img[0]
                        pix = fitz.Pixmap(doc, xref)
                        if pix.n < 5:
                            pix.save(others + file.split('.')[0] + str(page + 1) + '_'
                                     + str(total_images_on_page) + '.png')
                            total_images_on_page += 1
                        else:
                            pix1 = fitz.Pixmap(fitz.csRGB, pix)
                            pix1.save(others + file.split('.')[0] + str(page + 1) + '_'
                                     + str(total_images_on_page) + '.png')
                            total_images_on_page += 1
                        pix = None
            total_images_on_page = 0