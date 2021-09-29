import fitz
import os



class ITC_Type4:
    def check_blocks(self,blocks, list,s,e):
        dict = {}
        for i in range(s, e):
            temp = blocks[i]['lines'][0]['spans'][0]['text'].split(' ')[0]
            if (temp) in list:
                dict[temp] = i
        return dict


    def get_insured_and_agent_info(self,blocks):
        Insured_list = ['Name', 'Address', 'City,']
        Name = []
        Agent_Name = []
        Address = []
        Insured_dict = {}
        Agent_dict = {}
        Zip = []
        Producer_code =None
        block_dict = self.check_blocks(blocks, Insured_list,0,6)
        if blocks[block_dict['Name']]:
            end = [x for x in range(1, len(blocks[block_dict['Name']]['lines'])) if
                   blocks[block_dict['Name']]['lines'][x]['spans'][0]['text'] == 'Name']
            for x in range(1, end[0]):
                Name.append(blocks[block_dict['Name']]['lines'][x]['spans'][0]['text'])
            Name = ' '.join(map(str, Name)).strip()
            if len(blocks[block_dict['Name']]['lines']) < 10:
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

                end = [x for x in range(temp[0], len(blocks[block_dict['Name']]['lines'])) if
                       blocks[block_dict['Name']]['lines'][x]['spans'][0]['text'] == 'ZIP']
                for x in range(end[0] + 1, end[1]-1):
                    Zip.append(blocks[block_dict['Name']]['lines'][x]['spans'][0]['text'])

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
                        print(blocks[block_dict['Address'] + 2]['lines'][end[0]]['spans'][0]['text'])
                        for x in range(0, end[0] - 1):
                            Zip.append(blocks[block_dict['Address'] + 2]['lines'][x]['spans'][0]['text'])
                        if 'State ZIP ' in Zip:
                            Zip.remove('State ZIP ')

        Agent_list = ['Work', 'Phone', 'Work Number']
        block_dict = {}
        block_dict = self.check_blocks(blocks, Agent_list, 0, 9)
        if 'Work' in Agent_list :
            end = [x for x in range(1, len(blocks[block_dict['Work']]['lines'])) if
                   blocks[block_dict['Work']]['lines'][x]['spans'][0]['text'] == 'Producer' or
                   blocks[block_dict['Work']]['lines'][x]['spans'][0]['text'] == 'Producer Code']
            Producer_code = blocks[block_dict['Work']]['lines'][end[0]+2]['spans'][0]['text']


        Agent_dict['Producer Code'] = Producer_code
        Address = ' '.join(map(str, Address)).strip()
        Agent_Name = ' '.join(map(str, Agent_Name)).strip()

        Insured_dict['Insured Name'] = Name
        Insured_dict['Insured Address'] = Address
        Agent_dict['Agent Name'] = Agent_Name
        Insured_dict['City, State ZIP'] = ' '.join(map(str, Zip)).strip()
        if Insured_dict['City, State ZIP'] == '':
            print("hello")
        return Insured_dict, Agent_dict


    def get_company_info(self,blocks):
        list = [ 'Company','Policy','Rates']
        Company_dict = {}
        try:
            block_dict = self.check_blocks(blocks, list, 5, 9)
            if 'Company' in block_dict.keys():
                Company_dict['Company'] = blocks[block_dict['Company']]['lines'][1]['spans'][0]['text']
                end = [x for x in range(1, len(blocks[block_dict['Company']]['lines'])) if
                       blocks[block_dict['Company']]['lines'][x]['spans'][0]['text'] == 'Policy Term']
                Company_dict['Policy Term'] = blocks[block_dict['Company']]['lines'][end[0]+1]['spans'][0]['text']
            else:
                block_dict = self.check_blocks(blocks, list, 5, 13)
                if 'Company' in block_dict.keys():
                    Company_dict['Company'] = blocks[block_dict['Company']]['lines'][1]['spans'][0]['text']
                    if 'Policy' in block_dict.keys():
                        Company_dict['Policy Term'] = blocks[block_dict['Company']]['lines'][1]['spans'][0]['text']
                    else:
                        end = [x for x in range(1, len(blocks[block_dict['Company']]['lines'])) if
                               blocks[block_dict['Company']]['lines'][x]['spans'][0]['text'] == 'Policy Term']
                        Company_dict['Policy Term'] = blocks[block_dict['Company']]['lines'][end[0] + 1]['spans'][0]['text']
        except():
            pass
        return Company_dict


