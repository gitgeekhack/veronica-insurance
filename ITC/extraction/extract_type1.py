import fitz
import os

info_block = 4
Iname = 1
Aname = 5


class ITC_Type1:
    def check_blocks(self,blocks):
        for i in range(2, 5):
            if blocks[i]['lines'][Iname - 1]['spans'][0]['text'] == 'Name':
                return i
        return 0


    def get_insured_info(self,blocks, block_number):
        dict = {}
        i = block_number
        dict['Insured Name'] = blocks[i]['lines'][1]['spans'][0]['text']
        dict['Insured Address'] = blocks[i]['lines'][7]['spans'][0]['text']
        dict['Insured Zip code'] = blocks[i]['lines'][13]['spans'][0]['text']
        return dict


    def get_agent_info(self,blocks, block_number):
        dict = {}
        i = block_number
        dict['Agent Name'] = blocks[i]['lines'][Aname]['spans'][0]['text']
        if blocks[i]['lines'][16]['spans'][0]['text'] == 'City, State ZIP':
            text = blocks[i]['lines'][17]['spans'][0]['text']
        else:
            text = blocks[i]['lines'][16]['spans'][0]['text']
            text = text.split('City, State ZIP', 1)[1]
        dict['Agent Zip code'] = text
        if blocks[i]['lines'][34]['spans'][0]['text'] == 'Producer Code':
            text = blocks[i]['lines'][35]['spans'][0]['text']
        else:
            text = blocks[i]['lines'][31]['spans'][0]['text']
            text = text.split('Producer Code', 1)[1]
        dict["Producer Code"] = text.strip()
        return dict


    def get_company_info(self,blocks, block_number):
        i = block_number
        dict = {}
        if blocks[i]['lines'][42]['spans'][0]['text'] == 'Company':
            text = blocks[i]['lines'][43]['spans'][0]['text']
        else:
            text = blocks[i]['lines'][38]['spans'][0]['text']
        dict["Company"] = text
        if blocks[i]['lines'][50]['spans'][0]['text'] == 'Policy Term':
            text = blocks[i]['lines'][51]['spans'][0]['text']
        else:
            text = blocks[i]['lines'][46]['spans'][0]['text']
        dict["Policy Term"] = text
        return dict

    def get_driver_info(self,blocks,block_number):
        dict = {}
        list = []
        i=block_number
        text = blocks[i]['lines'][59]['spans'][0]['text']
        if text.split(' ')[0] == 'Veh':
            for j in range(59, 71):
                list.append(blocks[i]['lines'][j]['spans'][0]['text'])
        else:
            text = blocks[i]['lines'][54]['spans'][0]['text']
            if text.split(' ')[0] == 'Veh':
                for j in range(54, 66):
                    list.append(blocks[i]['lines'][j]['spans'][0]['text'])

        Vehlist = [x for x in list if "Veh" in x]
        DrvList = [x for x in list if "Drv" in x]
        dict['Vehicles'] = Vehlist
        dict['Drivers'] = DrvList
        l = len(DrvList)
        # print(l)
        list = [x for x in range(70, 100) if blocks[i]['lines'][x]['spans'][0]['text'] == 'Driver Information']
        list.extend([x for x in range(list[0], 100) if blocks[i]['lines'][x]['spans'][0]['text'] == 'Driver DOB'])
        Driver_info = []
        Driver_dob = []
        FR_filling = []
        Comp = []
        Coll = []
        for x in range(list[0] + 1, list[0] + l + 1): Driver_info.append(blocks[i]['lines'][x]['spans'][0]['text'])
        dict['Info'] = Driver_info

        for x in range(list[1] + 1, list[1] + l + 1): Driver_dob.append(blocks[i]['lines'][x]['spans'][0]['text'])
        dict['DOB'] = Driver_dob

        list.extend(
            [x for x in range(list[1] + l + 1, 120) if blocks[i]['lines'][x]['spans'][0]['text'] == 'FR Filing'])
        for x in range(list[2] + 1, list[2] + l + 1): FR_filling.append(blocks[i]['lines'][x]['spans'][0]['text'])
        dict['FR filling'] = FR_filling
        line_number = len(blocks[i]['lines'])

        text = [x for x in range(list[0], line_number) if
                blocks[i]['lines'][x]['spans'][0]['text'] == 'Comprehensive Deductible']
        v = len(Vehlist)
        if text:
            for x in range(text[0] + 1, text[0] + v + 1): Comp.append(blocks[i]['lines'][x]['spans'][0]['text'])
        dict['Comprehensive Deductible'] = Comp

        text = [x for x in range(list[0], line_number) if
                blocks[i]['lines'][x]['spans'][0]['text'] == 'Collision Deductible']
        if text:
            for x in range(text[0] + 1, text[0] + v + 1): Coll.append(blocks[i]['lines'][x]['spans'][0]['text'])

        dict['Collision Deductible'] = Coll
        text = []
        text = [x for x in range(list[0], line_number) if
                blocks[i]['lines'][x]['spans'][0]['text'] == 'Liability BI']
        if text:
            dict['Liability BI'] = blocks[i]['lines'][text[0] + 1]['spans'][0]['text']
        else:
            dict['Liability BI'] = None

        text = []
        text = [x for x in range(list[0], line_number) if
                blocks[i]['lines'][x]['spans'][0]['text'] == 'Liability PD']
        if text:
            dict['Liability PD'] = blocks[i]['lines'][text[0] + 1]['spans'][0]['text']
        else:
            dict['Liability PD'] = None

        text = []
        text = [x for x in range(list[0], line_number) if
                blocks[i]['lines'][x]['spans'][0]['text'] == 'Uninsured BI']
        if text:
            dict['Uninsured BI'] = blocks[i]['lines'][text[0] + 1]['spans'][0]['text']
        else:
            dict['Uninsured BI'] = None

        text = []
        text = [x for x in range(list[0], line_number) if
                blocks[i]['lines'][x]['spans'][0]['text'] == 'Unins PD/Coll Ded Waiver']
        if text:
            dict['Unins PD/Coll Ded Waiver'] = blocks[i]['lines'][text[0] + 1]['spans'][0]['text']
        else:
            dict['Unins PD/Coll Ded Waiver'] = None

        return dict

    def vehicle_info(self,blocks,i):
        text = []
        line_number = len(blocks[i + 1]['lines'])
        text = [x for x in range(0, line_number) if
                blocks[i + 1]['lines'][x]['spans'][0]['text'] == 'Vehicle Information']
        for x in range(0, line_number):
            if blocks[i + 1]['lines'][x]['spans'][0]['text'] == 'Vehicle Attributes':
                text.append(x)
        vehicle_info = []
        if text:
            for x in range(text[0] + 1, text[1]): vehicle_info.append(blocks[i + 1]['lines'][x]['spans'][0]['text'])
            dict['Vehicle Info'] = vehicle_info
        else:
            dict['Vehicle Info'] = None

        blocks = page.getText("dict")['blocks']
        blocks_number = len(blocks)
        x = 0
        i = 0
        block_num = 0
        line_num = 0
        for i, block in enumerate(blocks):
            try:
                for j, line in enumerate(block['lines']):
                    for span in line['spans']:
                        if span['text'] == 'Annual Miles Driven':
                            print('Annual Miles Driven: ', blocks[i]['lines'][j + 1]['spans'][0]['text'], i, j)
                            block_num = i
                            line_num = j
            except:
                pass
        v = len(Vehlist)

        Annual_miles = []
        if block_num > 0:
            for x in range(line_num + 1, line_num + v + 1):
                Annual_miles.append(blocks[block_num]['lines'][x]['spans'][0]['text'])
        else:
            print(f)

        print("Annual_miles:", Annual_miles)


