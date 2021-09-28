import fitz
import os

path = "D:/Office/veronica-self/ITC/out/line blocks_type2/"

def check_blocks(blocks,list):
    dict = {}
    for i in range(0, 10):
        if blocks[i]['lines'][0]['spans'][0]['text'] in list:
            dict[blocks[i]['lines'][0]['spans'][0]['text']] = i
    return dict

def get_personal_info(blocks):
    list = ['Name', 'Address', 'Work', 'Work Number', 'Company']
    Name = []
    Insured_dict ={}
    block_dict = check_blocks(blocks, list)
    if blocks[block_dict['Name']]:
        end = [x for x in range(1, len(blocks[block_dict['Name']]['lines'])) if
               blocks[block_dict['Name']]['lines'][x]['spans'][0]['text'] == '\xa0']
        for x in range(1, end[0]):
            Name.append(blocks[block_dict['Name']]['lines'][x]['spans'][0]['text'])
    Insured_dict['Insured Name'] = ' '.join(map(str, Name)).strip()
    return Insured_dict
for (root, dirs, file) in os.walk(path):
    for f in file:
        if '.pdf' in f:
            doc = fitz.open(path + f)
            page = doc[0]

            blocks = page.getText("dict")['blocks']
            Insured_dict = get_personal_info(blocks)
            print(Insured_dict)