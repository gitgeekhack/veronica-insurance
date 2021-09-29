import fitz
import os
import re

info_block = 4
Iname = 1
Aname = 5


class ITC_Type3:
    def check_blocks(self,blocks, list):
        dict = {}
        for i in range(0, 50):
            if blocks[i]['lines'][0]['spans'][0]['text'] in list:
                dict[blocks[i]['lines'][0]['spans'][0]['text']] = i
        return dict


    def get_insured_and_agent_info(self,blocks, block_dict):
        Insured_dict = {}
        Agent_dict = {}
        Name = []
        Agent_Name = []
        end = [x for x in range(1, len(blocks[block_dict['Name']]['lines'])) if
               blocks[block_dict['Name']]['lines'][x]['spans'][0]['text'] == 'Name']
        for x in range(1, end[0]):
            Name.append(blocks[block_dict['Name']]['lines'][x]['spans'][0]['text'])

        for x in range(end[0] + 1, len(blocks[block_dict['Name']]['lines'])):
            Agent_Name.append(blocks[block_dict['Name']]['lines'][x]['spans'][0]['text'])

        Insured_dict['Insured Name'] = ' '.join(map(str, Name)).strip()
        Agent_dict['Agent Name'] = ' '.join(map(str, Agent_Name)).strip()
        Address = []
        end = [x for x in range(1, len(blocks[block_dict['Address']]['lines'])) if
               blocks[block_dict['Address']]['lines'][x]['spans'][0]['text'] == 'Address']

        for x in range(1, end[0]): Address.append(blocks[block_dict['Address']]['lines'][x]['spans'][0]['text'])
        Insured_dict['Insured Address'] = ' '.join(map(str, Address)).strip()

        start = block_dict['Address']
        end = block_dict.get("Phone") or block_dict.get("Phone Number") or block_dict.get("Phone Number ( ) -")
        list = []
        for i in range(start + 1, end):
            for j in range(0, len(blocks[i]['lines'])):
                list.append(blocks[i]['lines'][j]['spans'][0]['text'])
        x = ' '.join(map(str, list)).strip()
        list = x.replace('City, State ZIP', '').split('\xa0 \xa0')
        Insured_dict['Insured Zip code'] = list[0].strip()
        Agent_dict['Agent Zip code'] = list[1].strip()
        producer_block = block_dict.get("Work") or block_dict.get("Work Number")
        Producer = []
        for x in range(0, len(blocks[producer_block]['lines'])): Producer.append(
            blocks[producer_block]['lines'][x]['spans'][0]['text'])
        list = ' '.join(map(str, Producer)).strip().replace('Producer Code', '').split('\xa0 \xa0')
        Agent_dict['Producer code'] = list[1].strip()
        return Insured_dict, Agent_dict


    def get_company_info(self,blocks, block_dict):
        Company_dict = {}
        Company_dict['Company'] = blocks[block_dict['Company']]['lines'][1]['spans'][0]['text']
        Company_dict['Policy Term'] = blocks[block_dict['Policy Term']]['lines'][1]['spans'][0]['text']
        return Company_dict


    def get_driver_info(self,blocks, block_dict):
        driver_info_dict = {}
        start = block_dict.get("Quote By")
        Vehlist = []
        Drvlist = []
        Drvinfo = []
        Drvdob = []
        FRfiling = []
        Comp = []
        Coll = []
        LiaBI = ''
        LiaPD = None
        UniBI = ''
        UniPD = None
        for x in range(0, len(blocks[start + 1]['lines'])): Vehlist.append(
            blocks[start + 1]['lines'][x]['spans'][0]['text'])
        Vehlist = [x for x in Vehlist if "Veh" in x]
        driver_info_dict['Vehicles'] = Vehlist

        for x in range(0, len(blocks[start + 2]['lines'])): Drvlist.append(
            blocks[start + 2]['lines'][x]['spans'][0]['text'])
        Drvlist = [x for x in Drvlist if "Drv" in x]
        driver_info_dict['Drivers'] = Drvlist

        l = max(len(Drvlist),len(Vehlist))
        for x in range(1, l + 1): Drvinfo.append(blocks[block_dict['Driver Information']]['lines'][x]['spans'][0]['text'])
        driver_info_dict['Driver Information'] = Drvinfo

        for x in range(1, l + 1): Drvdob.append(blocks[block_dict['Driver DOB']]['lines'][x]['spans'][0]['text'])
        driver_info_dict['Driver DOB'] = Drvdob

        for x in range(1, l + 1): FRfiling.append(blocks[block_dict['FR Filing']]['lines'][x]['spans'][0]['text'])
        driver_info_dict['FR Filing'] = FRfiling
        v = len(Vehlist)
        if 'Comprehensive Deductible' in block_dict.keys():
            for x in range(1, l + 1): Comp.append(
                blocks[block_dict['Comprehensive Deductible']]['lines'][x]['spans'][0]['text'])
        driver_info_dict['Comprehensive Deductible'] = Comp

        if 'Collision Deductible' in block_dict.keys():
            for x in range(1, l + 1): Coll.append(
                blocks[block_dict['Collision Deductible']]['lines'][x]['spans'][0]['text'])
        driver_info_dict['Collision Deductible'] = Coll

        if 'Liability BI' in block_dict.keys():
            LiaBI = blocks[block_dict['Liability BI']]['lines'][1]['spans'][0]['text']
        driver_info_dict['Liability BI'] = str(LiaBI)

        if 'Liability PD' in block_dict.keys():
            LiaPD = int(blocks[block_dict['Liability PD']]['lines'][1]['spans'][0]['text'])
        driver_info_dict['Liability PD'] = LiaPD

        if 'Uninsured BI' in block_dict.keys():
            UniBI = blocks[block_dict['Uninsured BI']]['lines'][1]['spans'][0]['text']
            temp = blocks[block_dict['Uninsured BI'] + 1]['lines'][0]['spans'][0]['text'].split(' ')
            if 'Unins PD/Coll Ded Waiver' in block_dict.keys():
                UniPD = blocks[block_dict['Unins PD/Coll Ded Waiver']]['lines'][2]['spans'][0]['text']
            elif 'Unins PD/Coll Ded' in block_dict.keys():
                UniPD = blocks[block_dict['Unins PD/Coll Ded']]['lines'][2]['spans'][0]['text']

            elif len(temp) == 5:
                UniPD = temp[-1]
        driver_info_dict['Uninsured BI'] = UniBI
        driver_info_dict['Unins PD/Coll Ded Wavier'] = UniPD
        return driver_info_dict



