import pytest

from datetime import date,datetime
from sepa_sctinst.schema_validation import SchemaValidation
from sepa_sctinst.sct_inst import SCTInst,GroupHeader,Transaction,Participant
from sepa_sctinst import Payment
from faker import Faker
fake = Faker()

schema_validation = SchemaValidation()


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

    assert response['isValid'] == True
    