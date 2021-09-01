from datetime import date,datetime
from sepa_sctinst.schema_validation import SchemaValidation
from sepa_sctinst.sct_inst_c2b import SCTInstC2B,GroupHeader,Transaction,PaymentInformation
from sepa_sctinst.participant import Participant
from faker import Faker
from sepa_sctinst.default_messages import DefaultMessages
import pytest

fake = Faker()

schema_validation = SchemaValidation()


def init_default_message():
    group_header = GroupHeader('MSGID1234',datetime.today(),'Initiator Name')
    originator = Participant('BOUSFRPPXXX','FR7630001007941234567890185','The originator company')
    beneficiary = Participant('BOUSFRPPXXX','FR7630001007941234567890185','My beneficiary company')
    payment_inf = PaymentInformation("Payment-Information-ID",True,date.today())
    transation = Transaction(beneficiary,10.12,'end to end instr','remittance information')
    transation_2 = Transaction(beneficiary,30.12,'end to end instr','remittance information')
    sct_message = SCTInstC2B(group_header,originator,payment_inf,[])
    sct_message.add_transaction(transation)
    sct_message.add_transaction(transation_2)
    return sct_message
    
      
def test_sct_inst_c2b_init():
    sct_message = init_default_message()
    assert len(sct_message.group_header.message_identification) > 1
    assert len(sct_message.originator.bic) > 1
    

    
def test_sct_inst_c2b_to_xml():
    sct_message = init_default_message()
    
    xml_message = sct_message.to_xml()
    response = schema_validation.validate(xml_message,DefaultMessages.SCTINST_C2B)

    assert response['isValid'] == True
    
def test_sct_inst_c2b_no_transaction():
    sct_message = init_default_message()
    sct_message.transactions = []
    
    with pytest.raises(ValueError):
        sct_message.to_xml()


    
def test_sct_inst_c2b_random():
    random_message = SCTInstC2B.random(4)
    response = schema_validation.validate(random_message.to_xml(),DefaultMessages.SCTINST_C2B)
    assert response['isValid'] == True
    
def test_sct_inst_to_interbank():
    random_message = SCTInstC2B.random(4)
    interbanks = random_message.to_interbank('CLRG')
    
    for message in interbanks:
        response = schema_validation.validate(message.to_xml(),DefaultMessages.SCTINST_INTERBANK)
        assert response['isValid'] == True
    assert len(interbanks) == 4
    