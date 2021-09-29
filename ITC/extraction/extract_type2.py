import fitz
import os


class ITC_Type2:
    def check_blocks(self, blocks, list, s, e):
        dict = {}
        for i in range(s, e):
            if blocks[i]['type'] == 0:
                temp = blocks[i]['lines'][0]['spans'][0]['text'].split(' ')[0]
                if (temp) in list:
                    dict[temp] = i
        return dict

    def get_personal_info(self, blocks):
        Insured_list = ['Name', 'Address', 'City,']
        Name = []
        Agent_Name = []
        Address = []
        Insured_dict = {}
        Agent_dict = {}
        Zip = []
        block_dict = self.check_blocks(blocks, Insured_list, 0, 7)
        if blocks[block_dict['Name']]:
            end = [x for x in range(1, len(blocks[block_dict['Name']]['lines'])) if
                   blocks[block_dict['Name']]['lines'][x]['spans'][0]['text'] == 'Name']
            for x in range(1, end[0]):
                Name.append(blocks[block_dict['Name']]['lines'][x]['spans'][0]['text'])
            Name = ' '.join(map(str, Name)).strip()
            if len(blocks[block_dict['Name']]['lines']) < 8:
                for x in range(end[0] + 1, len(blocks[block_dict['Name']]['lines'])):
                    Agent_Name.append(blocks[block_dict['Name']]['lines'][x]['spans'][0]['text'])
            else:
                temp = [x for x in range(end[0] + 1, len(blocks[block_dict['Name']]['lines'])) if
                        blocks[block_dict['Name']]['lines'][x]['spans'][0]['text'] == 'Address']
                for x in range(end[0] + 1, temp[0]):
                    Agent_Name.append(blocks[block_dict['Name']]['lines'][x]['spans'][0]['text'])
                end = []
                end = [x for x in range(temp[0], len(blocks[block_dict['Name']]['lines'])) if
                       blocks[block_dict['Name']]['lines'][x]['spans'][0]['text'] == 'Address']
                for x in range(end[0] + 1, end[1]):
                    Address.append(blocks[block_dict['Name']]['lines'][x]['spans'][0]['text'])

        if 'Address' in block_dict.keys():
            end = []
            temp = blocks[block_dict['Address']]['lines'][0]['spans'][0]['text'].split(' ')
            if len(temp) > 1:
                if temp[0] == 'Address':
                    Address = temp[1:]
            end = [x for x in range(1, len(blocks[block_dict['Address']]['lines'])) if
                   blocks[block_dict['Address']]['lines'][x]['spans'][0]['text'] == 'Address']
            for x in range(1, end[0]):
                Address.append(blocks[block_dict['Address']]['lines'][x]['spans'][0]['text'])
            end = []
            end = [x for x in range(1, len(blocks[block_dict['Address']]['lines'])) if
                   blocks[block_dict['Address']]['lines'][x]['spans'][0]['text'] == 'City,' or
                   blocks[block_dict['Address']]['lines'][x]['spans'][0]['text'] == 'City, State']

            if end:
                if len(end) == 2:
                    for x in range(end[0] + 1, end[1]):
                        block = blocks[block_dict['Address']]
                        line = block['lines'][x]
                        for j, span in enumerate(line['spans']):
                            Zip.append(span['text'])
                    if 'State ZIP ' in Zip:
                        Zip.remove('State ZIP ')
                    if 'ZIP' in Zip:
                        Zip.remove('ZIP')
                else:
                    for x in range(end[0], len(blocks[block_dict['Address'] + 1]['lines'])):
                        Zip.append(blocks[block_dict['Address'] + 1]['lines'][x]['spans'][0]['text'])
            else:
                if blocks[block_dict['Address'] + 1]['lines'][0]['spans'][0]['text'] == 'City,':
                    if len(blocks[block_dict['Address'] + 1]['lines']) == 2:
                        end = []
                        end = [x for x in range(1, len(blocks[block_dict['Address'] + 2]['lines'])) if
                               blocks[block_dict['Address'] + 2]['lines'][x]['spans'][0]['text'] == 'State ZIP']

                        for x in range(0, end[0] - 1):
                            Zip.append(blocks[block_dict['Address'] + 2]['lines'][x]['spans'][0]['text'])
                        if 'State ZIP ' in Zip:
                            Zip.remove('State ZIP ')
        Agent_list = ['Work', 'Phone', 'Work Number']
        block_dict = self.check_blocks(blocks, Agent_list, 0, 12)
        end = [x for x in range(1, len(blocks[block_dict['Work']]['lines'])) if
               blocks[block_dict['Work']]['lines'][x]['spans'][0]['text'] == 'Producer' or
               blocks[block_dict['Work']]['lines'][x]['spans'][0]['text'] == 'Producer Code']

        Agent_dict['Producer Code'] = blocks[block_dict['Work']]['lines'][end[0] + 2]['spans'][0]['text']
        Address = ' '.join(map(str, Address)).strip()
        Agent_Name = ' '.join(map(str, Agent_Name)).strip()

        Insured_dict['Insured Name'] = Name
        Insured_dict['Insured Address'] = Address
        Agent_dict['Agent Name'] = Agent_Name
        Insured_dict['City, State ZIP'] = ' '.join(map(str, Zip)).strip()
        return Insured_dict, Agent_dict

    def get_company_info(self, blocks):
        list = ['Company', 'Policy', 'Rates']
        Company_dict = {}
        try:
            block_dict = self.check_blocks(blocks, list, 5, 15)
            Company_dict['Company'] = blocks[block_dict['Company']]['lines'][1]['spans'][0]['text']
            if 'Policy' in block_dict.keys():
                Company_dict['Policy Term'] = blocks[block_dict['Policy']]['lines'][1]['spans'][0]['text']
            else:
                end = [x for x in range(1, len(blocks[block_dict['Rates']]['lines'])) if
                       blocks[block_dict['Rates']]['lines'][x]['spans'][0]['text'] == 'Policy Term']
                Company_dict['Policy Term'] = blocks[block_dict['Rates']]['lines'][end[0]]['spans'][0]['text']
        except:
            block_dict = self.check_blocks(blocks, list, 5, 10)
            Company_dict['Company'] = blocks[block_dict['Company']]['lines'][1]['spans'][0]['text']
            end = [x for x in range(1, len(blocks[block_dict['Company']]['lines'])) if
                   blocks[block_dict['Company']]['lines'][x]['spans'][0]['text'] == 'Policy Term']
            Company_dict['Policy Term'] = blocks[block_dict['Company']]['lines'][end[0] + 1]['spans'][0]['text']
        return Company_dict

    def get_driver_info(self, blocks):
        list = ['Company', 'ITC', 'Liability']
        Driver_info_list = []
        block_dict = self.check_blocks(blocks, list, 5, len(blocks))
        Driver_Information_dict = {}
        Driver_info = []
        Driver_DOB = []
        FR_filing = []
        Liability_BI = []
        Liability_PD = []
        Uninsured_BI = []
        Uninsured_PD = []
        Vehlist=[]
        Drvlist=[]
        Comprehensive_Deductible = []
        Collision_Deductible = []
        if 'ITC' in block_dict.keys():
            for x in range(0, len(blocks[block_dict['ITC'] - 1]['lines'])):
                Driver_info_list.append(blocks[block_dict['ITC'] - 1]['lines'][x]['spans'][0]['text'])
            m = int(len(Driver_info_list) / 2)
            Vehlist = Driver_info_list[:m]
            Drvlist = Driver_info_list[m:]
            Vehlist = [x for x in Vehlist if "Veh" in x]
            Drvlist = [x for x in Drvlist if "Drv" in x]

            l = max(len(Vehlist), len(Drvlist))
            Dinfo = []
            dob = []
            FR = []
            CompD = []
            CollD = []

            Dinfo = [x for x in range(1, len(blocks[block_dict['ITC']]['lines'])) if
                     blocks[block_dict['ITC']]['lines'][x]['spans'][0]['text'] == 'Driver Information']
            if Dinfo:
                dob = [x for x in range(Dinfo[0], len(blocks[block_dict['ITC']]['lines'])) if
                       blocks[block_dict['ITC']]['lines'][x]['spans'][0]['text'] == 'Driver DOB']

                for x in range(Dinfo[0] + 1, Dinfo[0] + l + 1): Driver_info.append(
                    blocks[block_dict['ITC']]['lines'][x]['spans'][0]['text'])

                for x in range(dob[0] + 1, dob[0] + l + 1): Driver_DOB.append(
                    blocks[block_dict['ITC']]['lines'][x]['spans'][0]['text'])

                FR = [x for x in range(Dinfo[0], len(blocks[block_dict['ITC']]['lines'])) if
                      blocks[block_dict['ITC']]['lines'][x]['spans'][0]['text'] == 'FR Filing']

                for x in range(FR[0] + 1, FR[0] + l + 1): FR_filing.append(
                    blocks[block_dict['ITC']]['lines'][x]['spans'][0]['text'])

                CompD = [x for x in range(FR[0], len(blocks[block_dict['ITC']]['lines'])) if
                         blocks[block_dict['ITC']]['lines'][x]['spans'][0]['text'] == 'Comprehensive Deductible']
                if CompD:
                    for x in range(CompD[0] + 1, CompD[0] + l + 1): Comprehensive_Deductible.append(
                        blocks[block_dict['ITC']]['lines'][x]['spans'][0]['text'])

                CollD = [x for x in range(FR[0], len(blocks[block_dict['ITC']]['lines'])) if
                         blocks[block_dict['ITC']]['lines'][x]['spans'][0]['text'] == 'Collision Deductible']
                if CollD:
                    for x in range(CollD[0] + 1, CollD[0] + l + 1): Collision_Deductible.append(
                        blocks[block_dict['ITC']]['lines'][x]['spans'][0]['text'])

                liBI = [x for x in range(0, len(blocks[block_dict['Liability']]['lines'])) if
                        blocks[block_dict['Liability']]['lines'][x]['spans'][0]['text'] == 'Liability BI']
                Liability_BI = blocks[block_dict['Liability']]['lines'][liBI[0] + 1]['spans'][0]['text']

                liPD = [x for x in range(0, len(blocks[block_dict['Liability']]['lines'])) if
                        blocks[block_dict['Liability']]['lines'][x]['spans'][0]['text'] == 'Liability PD']

                Liability_PD = blocks[block_dict['Liability']]['lines'][liPD[0] + 1]['spans'][0]['text']


        elif 'Company' in block_dict.keys():
            start = [x for x in range(1, len(blocks[block_dict['Company']]['lines'])) if
                     blocks[block_dict['Company']]['lines'][x]['spans'][0]['text'] == 'Lead Source']
            if start:
                end = [x for x in range(start[0], len(blocks[block_dict['Company']]['lines'])) if
                       blocks[block_dict['Company']]['lines'][x]['spans'][0]['text'] == 'ITC Transaction ID']
            for x in range(start[0] + 2, end[0]): Driver_info_list.append(
                blocks[block_dict['Company']]['lines'][x]['spans'][0]['text'])
            m = int(len(Driver_info_list) / 2)
            Vehlist = Driver_info_list[:m]
            Drvlist = Driver_info_list[m:]
            Vehlist = [x for x in Vehlist if "Veh" in x]
            Drvlist = [x for x in Drvlist if "Drv" in x]

            l = max(len(Vehlist), len(Drvlist))
            Dinfo = []
            dob = []
            FR = []
            liBI = []
            liPD = []
            UniBI = []
            UniPD = []
            Liability_PD = None
            Dinfo = [x for x in range(1, len(blocks[block_dict['Company']]['lines'])) if
                     blocks[block_dict['Company']]['lines'][x]['spans'][0]['text'] == 'Driver Information']
            if Dinfo:
                dob = [x for x in range(Dinfo[0], len(blocks[block_dict['Company']]['lines'])) if
                       blocks[block_dict['Company']]['lines'][x]['spans'][0]['text'] == 'Driver DOB']

                for x in range(Dinfo[0] + 1, Dinfo[0] + l + 1): Driver_info.append(
                    blocks[block_dict['Company']]['lines'][x]['spans'][0]['text'])

                for x in range(dob[0] + 1, dob[0] + l + 1): Driver_DOB.append(
                    blocks[block_dict['Company']]['lines'][x]['spans'][0]['text'])

                FR = [x for x in range(Dinfo[0], len(blocks[block_dict['Company']]['lines'])) if
                      blocks[block_dict['Company']]['lines'][x]['spans'][0]['text'] == 'FR Filing']

                for x in range(FR[0] + 1, FR[0] + l + 1): FR_filing.append(
                    blocks[block_dict['Company']]['lines'][x]['spans'][0]['text'])

                CompD = [x for x in range(Dinfo[0], len(blocks[block_dict['Company']]['lines'])) if
                         blocks[block_dict['Company']]['lines'][x]['spans'][0]['text'] == 'Comprehensive Deductible']
                if CompD:
                    for x in range(CompD[0] + 1, CompD[0] + l + 1): Comprehensive_Deductible.append(
                        blocks[block_dict['Company']]['lines'][x]['spans'][0]['text'])
                CollD = [x for x in range(Dinfo[0], len(blocks[block_dict['Company']]['lines'])) if
                         blocks[block_dict['Company']]['lines'][x]['spans'][0]['text'] == 'Collision Deductible']
                if CollD:
                    for x in range(CollD[0] + 1, CollD[0] + l + 1): Collision_Deductible.append(
                        blocks[block_dict['Company']]['lines'][x]['spans'][0]['text'])

                liBI = [x for x in range(FR[0], len(blocks[block_dict['Company']]['lines'])) if
                        blocks[block_dict['Company']]['lines'][x]['spans'][0]['text'] == 'Liability BI']
                Liability_BI = blocks[block_dict['Company']]['lines'][liBI[0] + 1]['spans'][0]['text']

                liPD = [x for x in range(FR[0], len(blocks[block_dict['Company']]['lines'])) if
                        blocks[block_dict['Company']]['lines'][x]['spans'][0]['text'] == 'Liability PD']

                Liability_PD = blocks[block_dict['Company']]['lines'][liPD[0] + 1]['spans'][0]['text']

                UniBI = [x for x in range(FR[0], len(blocks[block_dict['Company']]['lines'])) if
                         blocks[block_dict['Company']]['lines'][x]['spans'][0]['text'] == 'Uninsured BI']
                if UniBI:
                    Uninsured_BI = blocks[block_dict['Company']]['lines'][UniBI[0] + 1]['spans'][0]['text']

                UniPD = [x for x in range(FR[0], len(blocks[block_dict['Company']]['lines'])) if
                         blocks[block_dict['Company']]['lines'][x]['spans'][0]['text'] == 'Unins PD/Coll Ded Waiver']
                if UniPD:
                    Uninsured_PD = blocks[block_dict['Company']]['lines'][UniPD[0] + 1]['spans'][0]['text']
        Driver_Information_dict['Vehicles'] = Vehlist
        Driver_Information_dict['Drivers'] = Drvlist
        Driver_Information_dict['Driver Information'] = Driver_info
        Driver_Information_dict['Driver DOB'] = Driver_DOB
        Driver_Information_dict['FR filing'] = FR_filing
        Driver_Information_dict['Liability BI'] = Liability_BI
        Driver_Information_dict['Liability PD'] = Liability_PD
        Driver_Information_dict['Comprehensive Deductible'] = Comprehensive_Deductible
        Driver_Information_dict['Collision Deductible'] = Collision_Deductible
        Driver_Information_dict['Uninsured BI'] = Uninsured_BI
        Driver_Information_dict['Unins PD/Coll Ded Waiver'] = Uninsured_PD
        return Driver_Information_dict
