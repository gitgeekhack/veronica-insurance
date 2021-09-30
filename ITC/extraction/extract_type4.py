class ITC_Type4:
    def check_blocks(self, blocks, list, s, e):
        block_dict = {}
        for i in range(s, e):
            if blocks[i]['type'] == 0:
                temp = blocks[i]['lines'][0]['spans'][0]['text'].split(' ')[0]
                if (temp) in list:
                    block_dict[temp] = i
        return block_dict

    def get_insured_and_agent_info(self, blocks):
        insured_list = ['Name', 'Address', 'City,']
        insured_name = []
        agent_name = []
        insured_address = []
        insured_dict = {}
        agent_dict = {}
        zip_code = []
        producer_code = None
        block_dict = self.check_blocks(blocks, insured_list, 0, 7)
        if blocks[block_dict['Name']]:
            end = [x for x in range(1, len(blocks[block_dict['Name']]['lines'])) if
                   blocks[block_dict['Name']]['lines'][x]['spans'][0]['text'] == 'Name']
            for x in range(1, end[0]):
                insured_name.append(blocks[block_dict['Name']]['lines'][x]['spans'][0]['text'])
            insured_name = ' '.join(map(str, insured_name)).strip()
            if len(blocks[block_dict['Name']]['lines']) < 10:
                for x in range(end[0] + 1, len(blocks[block_dict['Name']]['lines'])):
                    agent_name.append(blocks[block_dict['Name']]['lines'][x]['spans'][0]['text'])
            else:
                temp = [x for x in range(end[0] + 1, len(blocks[block_dict['Name']]['lines'])) if
                        blocks[block_dict['Name']]['lines'][x]['spans'][0]['text'] == 'Address']
                for x in range(end[0] + 1, temp[0]):
                    agent_name.append(blocks[block_dict['Name']]['lines'][x]['spans'][0]['text'])
                end = []
                end = [x for x in range(temp[0], len(blocks[block_dict['Name']]['lines'])) if
                       blocks[block_dict['Name']]['lines'][x]['spans'][0]['text'] == 'Address']
                for x in range(end[0] + 1, end[1]):
                    insured_address.append(blocks[block_dict['Name']]['lines'][x]['spans'][0]['text'])

                end = [x for x in range(temp[0], len(blocks[block_dict['Name']]['lines'])) if
                       blocks[block_dict['Name']]['lines'][x]['spans'][0]['text'] == 'ZIP']
                for x in range(end[0] + 1, end[1] - 1):
                    zip_code.append(blocks[block_dict['Name']]['lines'][x]['spans'][0]['text'])

        if 'Address' in block_dict.keys():
            end = []
            temp = blocks[block_dict['Address']]['lines'][0]['spans'][0]['text'].split(' ')
            if len(temp) > 1:
                if temp[0] == 'Address':
                    insured_address = temp[1:]
            end = [x for x in range(1, len(blocks[block_dict['Address']]['lines'])) if
                   blocks[block_dict['Address']]['lines'][x]['spans'][0]['text'] == 'Address']
            for x in range(1, end[0]):
                insured_address.append(blocks[block_dict['Address']]['lines'][x]['spans'][0]['text'])
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
                            zip_code.append(span['text'])
                    if 'State ZIP ' in zip_code:
                        zip_code.remove('State ZIP ')
                    if 'ZIP' in zip_code:
                        zip_code.remove('ZIP')
                else:
                    for x in range(end[0], len(blocks[block_dict['Address'] + 1]['lines'])):
                        zip_code.append(blocks[block_dict['Address'] + 1]['lines'][x]['spans'][0]['text'])
            else:
                if blocks[block_dict['Address'] + 1]['lines'][0]['spans'][0]['text'] == 'City,':
                    if len(blocks[block_dict['Address'] + 1]['lines']) == 2:
                        end = []
                        end = [x for x in range(1, len(blocks[block_dict['Address'] + 2]['lines'])) if
                               blocks[block_dict['Address'] + 2]['lines'][x]['spans'][0]['text'] == 'State ZIP']

                        for x in range(0, end[0] - 1):
                            zip_code.append(blocks[block_dict['Address'] + 2]['lines'][x]['spans'][0]['text'])
                        if 'State ZIP ' in zip_code:
                            zip_code.remove('State ZIP ')

        agent_list = ['Work', 'Phone', 'Work Number']
        block_dict = {}
        block_dict = self.check_blocks(blocks, agent_list, 0, len(blocks))
        if 'Work' in agent_list:
            end = [x for x in range(1, len(blocks[block_dict['Work']]['lines'])) if
                   blocks[block_dict['Work']]['lines'][x]['spans'][0]['text'] == 'Producer' or
                   blocks[block_dict['Work']]['lines'][x]['spans'][0]['text'] == 'Producer Code']
            producer_code = blocks[block_dict['Work']]['lines'][end[0] + 2]['spans'][0]['text']

        agent_dict['Producer Code'] = producer_code
        insured_address = ' '.join(map(str, insured_address)).strip()
        agent_name = ' '.join(map(str, agent_name)).strip()

        insured_dict['Insured Name'] = insured_name
        insured_dict['Insured Address'] = insured_address
        agent_dict['Agent Name'] = agent_name
        insured_dict['City, State ZIP'] = ' '.join(map(str, zip_code)).strip()

        return insured_dict, agent_dict

    def get_company_info(self, blocks):
        text_list = ['Company', 'Policy', 'Rates']
        company_info_dict = {}

        block_dict = self.check_blocks(blocks, text_list, 5, len(blocks))
        if 'Company' in block_dict.keys() and not 'Policy' in block_dict.keys():
            company_info_dict['Company'] = blocks[block_dict['Company']]['lines'][1]['spans'][0]['text']
            end = [x for x in range(1, len(blocks[block_dict['Company']]['lines'])) if
                   blocks[block_dict['Company']]['lines'][x]['spans'][0]['text'] == 'Policy Term']
            if end:
                company_info_dict['Policy Term'] = blocks[block_dict['Company']]['lines'][end[0] + 1]['spans'][0]['text']
        else:
            block_dict = self.check_blocks(blocks, text_list, 5, len(blocks))
            if 'Company' in block_dict.keys():
                company_info_dict['Company'] = blocks[block_dict['Company']]['lines'][1]['spans'][0]['text']
                if 'Policy' in block_dict.keys():
                    company_info_dict['Policy Term'] = blocks[block_dict['Policy']]['lines'][1]['spans'][0]['text']
                else:
                    end = [x for x in range(1, len(blocks[block_dict['Company']]['lines'])) if
                           blocks[block_dict['Company']]['lines'][x]['spans'][0]['text'] == 'Policy Term']
                    company_info_dict['Policy Term'] = blocks[block_dict['Company']]['lines'][end[0] + 1]['spans'][0]['text']

        return company_info_dict

    def get_driver_info(self, blocks):
        text_list = ['Company', 'ITC', 'Liability']
        driver_info_list = []
        block_dict = self.check_blocks(blocks, text_list, 5, len(blocks))
        driver_information_dict = {}
        driver_info = []
        driver_dob = []
        fr_filing = []
        liability_bi = []
        liability_pd = []
        uninsured_bi = []
        uninsured_pd = []
        comprehensive_deductible = []
        collision_deductible = []
        if 'ITC' in block_dict.keys():
            for x in range(0, len(blocks[block_dict['ITC'] - 1]['lines'])):
                driver_info_list.append(blocks[block_dict['ITC'] - 1]['lines'][x]['spans'][0]['text'])
            m = int(len(driver_info_list) / 2)
            veh_list = driver_info_list[:m]
            drv_list = driver_info_list[m:]
            veh_list = [x for x in veh_list if "Veh" in x]
            drv_list = [x for x in drv_list if "Drv" in x]

            l = max(len(veh_list), len(drv_list))
            drv_info = []
            dob = []
            fr = []
            comp_deductible = []
            coll_deductible = []

            drv_info = [x for x in range(1, len(blocks[block_dict['ITC']]['lines'])) if
                        blocks[block_dict['ITC']]['lines'][x]['spans'][0]['text'] == 'Driver Information']
            if drv_info:
                dob = [x for x in range(drv_info[0], len(blocks[block_dict['ITC']]['lines'])) if
                       blocks[block_dict['ITC']]['lines'][x]['spans'][0]['text'] == 'Driver DOB']

                for x in range(drv_info[0] + 1, drv_info[0] + l + 1): driver_info.append(
                    blocks[block_dict['ITC']]['lines'][x]['spans'][0]['text'])

                for x in range(dob[0] + 1, dob[0] + l + 1): driver_dob.append(
                    blocks[block_dict['ITC']]['lines'][x]['spans'][0]['text'])

                fr = [x for x in range(drv_info[0], len(blocks[block_dict['ITC']]['lines'])) if
                      blocks[block_dict['ITC']]['lines'][x]['spans'][0]['text'] == 'FR Filing']

                for x in range(fr[0] + 1, fr[0] + l + 1): fr_filing.append(
                    blocks[block_dict['ITC']]['lines'][x]['spans'][0]['text'])

                comp_deductible = [x for x in range(fr[0], len(blocks[block_dict['ITC']]['lines'])) if
                                   blocks[block_dict['ITC']]['lines'][x]['spans'][0][
                                       'text'] == 'Comprehensive Deductible']
                if comp_deductible:
                    for x in range(comp_deductible[0] + 1, comp_deductible[0] + l + 1): comprehensive_deductible.append(
                        blocks[block_dict['ITC']]['lines'][x]['spans'][0]['text'])

                coll_deductible = [x for x in range(fr[0], len(blocks[block_dict['ITC']]['lines'])) if
                                   blocks[block_dict['ITC']]['lines'][x]['spans'][0]['text'] == 'Collision Deductible']
                if coll_deductible:
                    for x in range(coll_deductible[0] + 1, coll_deductible[0] + l + 1): collision_deductible.append(
                        blocks[block_dict['ITC']]['lines'][x]['spans'][0]['text'])

                liBI = [x for x in range(0, len(blocks[block_dict['Liability']]['lines'])) if
                        blocks[block_dict['Liability']]['lines'][x]['spans'][0]['text'] == 'Liability BI']
                liability_bi = blocks[block_dict['Liability']]['lines'][liBI[0] + 1]['spans'][0]['text']

                liPD = [x for x in range(0, len(blocks[block_dict['Liability']]['lines'])) if
                        blocks[block_dict['Liability']]['lines'][x]['spans'][0]['text'] == 'Liability PD']

                liability_pd = blocks[block_dict['Liability']]['lines'][liPD[0] + 1]['spans'][0]['text']


        elif 'Company' in block_dict.keys():
            start = [x for x in range(1, len(blocks[block_dict['Company']]['lines'])) if
                     blocks[block_dict['Company']]['lines'][x]['spans'][0]['text'] == 'Lead Source']
            if start:
                end = [x for x in range(start[0], len(blocks[block_dict['Company']]['lines'])) if
                       blocks[block_dict['Company']]['lines'][x]['spans'][0]['text'] == 'ITC Transaction ID']
            for x in range(start[0] + 2, end[0]): driver_info_list.append(
                blocks[block_dict['Company']]['lines'][x]['spans'][0]['text'])
            m = int(len(driver_info_list) / 2)
            veh_list = driver_info_list[:m]
            drv_list = driver_info_list[m:]
            veh_list = [x for x in veh_list if "Veh" in x]
            drv_list = [x for x in drv_list if "Drv" in x]

            l = max(len(veh_list), len(drv_list))
            drv_info = []
            dob = []
            fr = []
            liBI = []
            liPD = []
            uni_bi = []
            uni_pd = []
            liability_pd = None
            drv_info = [x for x in range(1, len(blocks[block_dict['Company']]['lines'])) if
                        blocks[block_dict['Company']]['lines'][x]['spans'][0]['text'] == 'Driver Information']
            if drv_info:
                dob = [x for x in range(drv_info[0], len(blocks[block_dict['Company']]['lines'])) if
                       blocks[block_dict['Company']]['lines'][x]['spans'][0]['text'] == 'Driver DOB']

                for x in range(drv_info[0] + 1, drv_info[0] + l + 1): driver_info.append(
                    blocks[block_dict['Company']]['lines'][x]['spans'][0]['text'])

                for x in range(dob[0] + 1, dob[0] + l + 1): driver_dob.append(
                    blocks[block_dict['Company']]['lines'][x]['spans'][0]['text'])

                fr = [x for x in range(drv_info[0], len(blocks[block_dict['Company']]['lines'])) if
                      blocks[block_dict['Company']]['lines'][x]['spans'][0]['text'] == 'FR Filing']

                for x in range(fr[0] + 1, fr[0] + l + 1): fr_filing.append(
                    blocks[block_dict['Company']]['lines'][x]['spans'][0]['text'])

                comp_deductible = [x for x in range(drv_info[0], len(blocks[block_dict['Company']]['lines'])) if
                                   blocks[block_dict['Company']]['lines'][x]['spans'][0][
                                       'text'] == 'Comprehensive Deductible']
                if comp_deductible:
                    for x in range(comp_deductible[0] + 1, comp_deductible[0] + l + 1): comprehensive_deductible.append(
                        blocks[block_dict['Company']]['lines'][x]['spans'][0]['text'])
                coll_deductible = [x for x in range(drv_info[0], len(blocks[block_dict['Company']]['lines'])) if
                                   blocks[block_dict['Company']]['lines'][x]['spans'][0][
                                       'text'] == 'Collision Deductible']
                if coll_deductible:
                    for x in range(coll_deductible[0] + 1, coll_deductible[0] + l + 1): collision_deductible.append(
                        blocks[block_dict['Company']]['lines'][x]['spans'][0]['text'])

                liBI = [x for x in range(fr[0], len(blocks[block_dict['Company']]['lines'])) if
                        blocks[block_dict['Company']]['lines'][x]['spans'][0]['text'] == 'Liability BI']
                liability_bi = blocks[block_dict['Company']]['lines'][liBI[0] + 1]['spans'][0]['text']

                liPD = [x for x in range(fr[0], len(blocks[block_dict['Company']]['lines'])) if
                        blocks[block_dict['Company']]['lines'][x]['spans'][0]['text'] == 'Liability PD']

                liability_pd = blocks[block_dict['Company']]['lines'][liPD[0] + 1]['spans'][0]['text']

                uni_bi = [x for x in range(fr[0], len(blocks[block_dict['Company']]['lines'])) if
                          blocks[block_dict['Company']]['lines'][x]['spans'][0]['text'] == 'Uninsured BI']
                if uni_bi:
                    uninsured_bi = blocks[block_dict['Company']]['lines'][uni_bi[0] + 1]['spans'][0]['text']

                uni_pd = [x for x in range(fr[0], len(blocks[block_dict['Company']]['lines'])) if
                          blocks[block_dict['Company']]['lines'][x]['spans'][0]['text'] == 'Unins PD/Coll Ded Waiver']
                if uni_pd:
                    uninsured_pd = blocks[block_dict['Company']]['lines'][uni_pd[0] + 1]['spans'][0]['text']
        driver_information_dict['Vehicles'] = veh_list
        driver_information_dict['Drivers'] = drv_list
        driver_information_dict['Driver Information'] = driver_info
        driver_information_dict['Driver DOB'] = driver_dob
        driver_information_dict['FR filing'] = fr_filing
        driver_information_dict['Liability BI'] = liability_bi
        driver_information_dict['Liability PD'] = liability_pd
        driver_information_dict['Comprehensive Deductible'] = comprehensive_deductible
        driver_information_dict['Collision Deductible'] = collision_deductible
        driver_information_dict['Uninsured BI'] = uninsured_bi
        driver_information_dict['Unins PD/Coll Ded Waiver'] = uninsured_pd
        return driver_information_dict
