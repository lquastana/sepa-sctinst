from datetime import date,datetime
from sepa_sctinst.schema_validation import SchemaValidation
from sepa_sctinst.sct_inst import SCTInst,GroupHeader,Transaction,Participant
from sepa_sctinst import Payment
from faker import Faker

import pytest

fake = Faker()

schema_validation = SchemaValidation()
message_empty = 'Document is empty'

@pytest.mark.parametrize(
    "filename,message_type,is_valid,error_msg_present,expected_message",[
        ('tests/sct_inst_files/pacs008_valid.xml',Payment.SCTINST, True, False,None), 
        ('tests/sct_inst_files/pacs008_invalid.xml',Payment.SCTINST, False, True,None), 
        ('tests/sct_inst_files/pacs008_empty.xml',Payment.SCTINST, False, True,message_empty)
    ]
)
def test_pacs008_xsd(filename,message_type,is_valid,error_msg_present,expected_message):

    with open(filename, 'r') as input:
        data = input.read()
    response = schema_validation.validate(data,message_type)

    assert response['isValid'] == is_valid
    assert ('error_messages' in response) == error_msg_present

    if expected_message is not None:
        messages_matched = filter(lambda x: expected_message in x, response['error_messages'])
        assert any(messages_matched)


def init_default_message():
    group_header = GroupHeader('MSGID1234',datetime.today(),date.today(),'CLRG')
    originator = Participant('BOUSFRPPXXX','FR7630001007941234567890185','The originator company')
    beneficiary = Participant('BOUSFRPPXXX','FR7630001007941234567890185','My beneficiary company')
    transation = Transaction(beneficiary,10.12,'end to end instr','tx id',datetime.now(),'reference','remittance information')
    sct_message = SCTInst(group_header,originator,transation)
    return sct_message
    
      
def test_pacs008_init():
    sct_message = init_default_message()
    assert len(sct_message.group_header.message_identification) > 1
    assert len(sct_message.originator.bic) > 1
    

    
def test_pacs008_to_xml():
    sct_message = init_default_message()
    
    xml_message = sct_message.to_xml()
    response = schema_validation.validate(xml_message,Payment.SCTINST)

    assert response['isValid'] == True


    
def test_sct_inst_random():
    random_message = SCTInst.random()
    response = schema_validation.validate(random_message.to_xml(),Payment.SCTINST)
    print(response)

    assert response['isValid'] == True
    