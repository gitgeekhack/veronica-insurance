import fitz
from extract_type1 import ITC_Type1
from extract_type2 import ITC_Type2
from extract_type3 import ITC_Type3
from extract_type4 import ITC_Type4


path = 'D:/Office/veronica-self/ITC/files/ITC examples 9-28-21/ITC CCS.pdf'

doc = fitz.open(path)
page = doc[0]
blocks = page.getText("dict")['blocks']

length_blocks = len(blocks)


if length_blocks>5 and length_blocks<9:
    type1 = ITC_Type1()
    i = type1.check_blocks(blocks)
    print("----INSURED INFO-----")
    insured_info = type1.get_insured_info(blocks, i)
    print(insured_info)
    print("----AGENT INFO-----")
    agent_info = type1.get_agent_info(blocks, i)
    print(agent_info)
    print("----COMPANY INFO----")
    company_info = type1.get_company_info(blocks, i)
    print(company_info)
    driver_info,vehicle_info = type1.get_driver_and_vehicle_info(blocks,i)
    print("----Driver INFO----")
    print(driver_info)
    print("----Vehicle INFO----")
    print(vehicle_info)
    print("------------------------------------------------------------")
elif length_blocks == 17:
    type2 = ITC_Type2()
    blocks = page.getText("dict")['blocks']
    insured_info, agent_info = type2.get_insured_and_agent_info(blocks)
    print("----Insured INFO-----")
    print(insured_info)
    print("----Agent INFO----")
    print(agent_info)
    print("----Company INFO----")
    company_info = type2.get_company_info(blocks)
    print(company_info)
    print("------------------------------------------------------------")
elif length_blocks >= 11 and length_blocks<25:
    type4 = ITC_Type4()
    blocks = page.getText("dict")['blocks']
    insured_info, agent_info = type4.get_insured_and_agent_info(blocks)
    print("----Insured INFO-----")
    print(insured_info)
    print("----Agent INFO----")
    print(agent_info)
    print("----Company INFO----")
    company_info = type4.get_company_info(blocks)
    print(company_info)
    print("------------------------------------------------------------")
elif length_blocks>=40:
    type3 = ITC_Type3()
    blocks = page.getText("dict")['blocks']
    list = ['Name', 'Address', 'Phone Number', 'Phone', 'Phone Number ( ) -', 'Work', 'Work Number', 'Company',
            'Policy Term', 'Quote By', 'Driver Information', 'Driver DOB', 'FR Filing',
            'Comprehensive Deductible',
            'Collision Deductible', 'Liability BI', 'Liability PD', 'Uninsured BI', 'Unins PD/Coll Ded',
            'Unins PD/Coll Ded Waiver']
    block_dict = type3.check_blocks(blocks, list)
    print("----PERSONAL INFO-----")
    insured_info, agent_info = type3.get_insured_and_agent_info(blocks, block_dict)
    print(insured_info)
    print(agent_info)
    print("----Company INFO-----")
    company_info = type3.get_company_info(blocks, block_dict)
    print(company_info)
    driver_info,vehicle_info = type3.get_driver_and_vehicle_info(blocks,block_dict,doc)
    print("----Driver INFO----")
    print(driver_info)
    print("----Vehicle INFO----")
    print(vehicle_info)
    print("------------------------------------------------------------")
