import pytest

from datetime import date

from sctinst.schema_validation import SchemaValidation
from sctinst.pacs008 import SCTInst,IbanData,Transaction

schema_validation = SchemaValidation()

message_type_not_found = 'Message type not found.'
message_empty = 'Document is empty'

@pytest.mark.parametrize(
    "filename,message_type,is_valid,error_msg_present,expected_message",[
        ('sctinst/test/pacs008_files/pacs008_valid.xml','TOTOInst', False, True,message_type_not_found), 
        ('sctinst/test/pacs008_files/pacs008_valid.xml','SCTInst', True, False,None), 
        ('sctinst/test/pacs008_files/pacs008_invalid.xml','SCTInst', False, True,None), 
        ('sctinst/test/pacs008_files/pacs008_empty.xml','SCTInst', False, True,message_empty)
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
    message_identification='msg_id',
    initiating_party_name='Your name',
    debtor = IbanData('BOUSFRPPXXX','FR7630001007941234567890185','My company')
    sct_message = SCTInst(message_identification,initiating_party_name,debtor)
    
    assert sct_message.message_identification == message_identification
    assert sct_message.initiating_party_name == initiating_party_name
    assert sct_message.debtor == debtor
    
def test_pacs008_add_transaction():
    message_identification='msg_id',
    initiating_party_name='Your name',
    debtor = IbanData('BOUSFRPPXXX','FR7630001007941234567890185','My company')
    sct_message = SCTInst(message_identification,initiating_party_name,debtor)
    
    transation = Transaction(
        name = 'Name of the creditor',
        bic = 'BOUSFRPPXXX',
        iban = 'FR7630001007941234567890185',
        amount = 100.12,
        instruction = '12345',
        reference = 'XYZ-1234/123',
        remittance_information = 'remittance_information',
        requested_date = date(2002, 12, 4),
        )
    sct_message.add_transaction(transation)
    
    assert sct_message.message_identification == message_identification
    assert sct_message.initiating_party_name == initiating_party_name
    assert sct_message.debtor == debtor
    assert len(sct_message.transactions) == 1