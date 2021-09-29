import fitz
from extract_type1 import ITC_Type1
from extract_type2 import ITC_Type2
from extract_type3 import ITC_Type3
from extract_type4 import ITC_Type4


path = 'D:/Office/veronica-self/ITC/new_out/out_ITC TurboRater - Breakdown[Edgar Silva].pdf.pdf'

doc = fitz.open(path)
page = doc[0]
blocks = page.getText("dict")['blocks']

length_blocks = len(blocks)


if length_blocks>5 and length_blocks<9:
    type1 = ITC_Type1()
    i = type1.check_blocks(blocks)
    print("----INSURED INFO-----")
    Insured_info = type1.get_insured_info(blocks, i)
    print(Insured_info)
    print("----AGENT INFO-----")
    Agent_info = type1.get_agent_info(blocks, i)
    print(Agent_info)
    print("----COMPANY INFO----")
    Company_info = type1.get_company_info(blocks, i)
    print(Company_info)
    print("------------------------------------------------------------")
elif length_blocks == 17:
    type2 = ITC_Type2()
    blocks = page.getText("dict")['blocks']
    Insured_dict, Agent_dict = type2.get_insured_and_agent_info(blocks)
    print("----Insured INFO-----")
    print(Insured_dict)
    print("----Agent INFO----")
    print(Agent_dict)
    print("----Company INFO----")
    Company_dict = type2.get_company_info(blocks)
    print(Company_dict)
    print("------------------------------------------------------------")
elif length_blocks >= 11 and length_blocks<25:
    type4 = ITC_Type4()
    blocks = page.getText("dict")['blocks']
    Insured_dict, Agent_dict = type4.get_insured_and_agent_info(blocks)
    print("----Insured INFO-----")
    print(Insured_dict)
    print("----Agent INFO----")
    print(Agent_dict)
    print("----Company INFO----")
    Company_dict = type4.get_company_info(blocks)
    print(Company_dict)
    print("------------------------------------------------------------")
elif length_blocks>=40:
    type3 = ITC_Type3()
    blocks = page.getText("dict")['blocks']
    list = ['Name', 'Address', 'Phone Number', 'Phone', 'Phone Number ( ) -', 'Work', 'Work Number', 'Company',
            'Policy Term', 'Quote By', 'Driver Information', 'Driver DOB', 'FR Filing',
            'Comprehensive Deductible',
            'Collision Deductible', 'Liability BI', 'Liability PD', 'Uninsured BI', 'Unins PD/Coll Ded',
            'Unins PD/Coll Ded Waiver']
    print(len(blocks))
    block_dict = type3.check_blocks(blocks, list)
    print("----PERSONAL INFO-----")
    Insured_info, Agent_info = type3.get_insured_and_agent_info(blocks, block_dict)
    print(Insured_info)
    print(Agent_info)
    print("----Company INFO-----")
    Company_info = type3.get_company_info(blocks, block_dict)
    print(Company_info)
    print("------------------------------------------------------------")
