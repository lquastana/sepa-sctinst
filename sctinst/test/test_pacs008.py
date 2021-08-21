import pytest

from datetime import date,datetime
from sctinst.schema_validation import SchemaValidation
from sctinst.pacs008 import SCTInst,GroupHeader,Transaction,Participant
from sctinst import Payment

schema_validation = SchemaValidation()

message_type_not_found = 'Message type not found.'
message_empty = 'Document is empty'

def init_default_message_without_transactions():
    group_header = GroupHeader('MSGID1234',datetime.today(),date.today(),'CLRG')
    originator = Participant('BOUSFRPPXXX','FR7630001007941234567890185','The originator company')
    sct_message = SCTInst(group_header,originator)
    return sct_message

def init_default_message_with_transactions(transactions):
    group_header = GroupHeader('MSGID1234',datetime.today(),date.today(),'CLRG')
    originator = Participant('BOUSFRPPXXX','FR7630001007941234567890185','The originator company')
    sct_message = SCTInst(group_header,originator,transactions)
    return sct_message
    

    
def init_default_transaction():
    beneficiary = Participant('BOUSFRPPXXX','FR7630001007941234567890185','My beneficiary company')
    transation = Transaction(beneficiary,10.12,'end to end instr','tx id',datetime.now(),'reference','remittance information')
    return transation
    
    

@pytest.mark.parametrize(
    "filename,message_type,is_valid,error_msg_present,expected_message",[
        ('sctinst/test/pacs008_files/pacs008_valid.xml',Payment.SCTINST, True, False,None), 
        ('sctinst/test/pacs008_files/pacs008_invalid.xml',Payment.SCTINST, False, True,None), 
        ('sctinst/test/pacs008_files/pacs008_empty.xml',Payment.SCTINST, False, True,message_empty)
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
        
        
def test_pacs008_init():
    
    sct_message = init_default_message_without_transactions()
    
    
    assert len(sct_message.group_header.message_identification) > 1
    assert len(sct_message.originator.bic) > 1
    
def test_pacs008_add_transaction():
    sct_message = init_default_message_without_transactions()
    sct_message.add_transaction(init_default_transaction())
    assert len(sct_message.transactions) == 1
    
def test_pacs008_one_transaction_to_xml():
    sct_message = init_default_message_with_transactions([init_default_transaction()])
    
    xml_message = sct_message.to_xml()
    response = schema_validation.validate(xml_message,Payment.SCTINST)

    assert response['isValid'] == True
    
def test_pacs008_no_transaction_to_xml():
    sct_message = init_default_message_without_transactions()
    
    with pytest.raises(ValueError):
        sct_message.to_xml()

    
def test_pacs008_two_transactions_to_xml():
    sct_message = init_default_message_without_transactions()
    sct_message.add_transaction(init_default_transaction())
    sct_message.add_transaction(init_default_transaction())
    xml_message = sct_message.to_xml()
    response = schema_validation.validate(xml_message,Payment.SCTINST)

    assert response['isValid'] == False
    