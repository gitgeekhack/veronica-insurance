import pprint
import ocrmypdf
import xmltodict
import fitz

doc = fitz.open('/home/nirav/PycharmProjects/underwriting_automation/app/data/temp/example/application/ALLIANCE_APP_Alfonso Soto.pdf')

# ocrmypdf.ocr('/home/nirav/PycharmProjects/underwriting_automation/app/data/temp/example/application/ALLIANCE_APP_AARON ROSS.pdf', 'converted.pdf')

width = float(doc[0].bound().x1)
height = float(doc[0].bound().y1)

with open('/home/nirav/Downloads/alliance (2)/annotations.xml', 'r', encoding='utf-8') as file:
    my_xml = file.read()

# Use xmltodict to parse and convert
# the XML document
my_dict = xmltodict.parse(my_xml)

data = {}
for i in my_dict['annotations']['image']:
    try:
        page_no = int(i['@id'])
        if isinstance(i['box'], list):
            data[page_no] = {}
            for j in i['box']:
                data[page_no][j['@label']] = [0.36 * float(j['@xtl']), 0.36 * float(j['@ytl']),
                                              0.36 * float(j['@xbr']), 0.36 * float(j['@ybr'])]
        else:
            data[page_no] = {}
            data[page_no][i['box']['@label']] = [0.36 * float(i['box']['@xtl']), 0.36 * float(i['box']['@ytl']),
                                                 0.36 * float(i['box']['@xbr']), 0.36 * float(i['box']['@ybr'])]
    except:
        pass

selected_page = doc[2]

# drivers_start = selected_page.get_textbox(data[2]['drivers_start'])
# drivers_end = selected_page.get_textbox(data[2]['drivers_end'])

drivers_start = 'Drivers and Household Residents'
drivers_end = 'Driving History'


blocks = selected_page.get_text('blocks')
starting_box = None
ending_box = None

for block in blocks:
    if drivers_start in block[4]:
        starting_box = block[:4]
    elif drivers_end in block[4]:
        ending_box = block[:4]

# print(starting_box)
# print(ending_box)

required_data_box = fitz.Rect([starting_box[0], starting_box[3], 612.0, ending_box[1]])
text = selected_page.get_textbox(required_data_box)
print(required_data_box)

# print(text)
# print(text.find('1.'))
# print(text[:143])

# pprint.pprint(blocks)
