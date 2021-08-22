from sepa_sctinst.schema_validation import SchemaValidation
from sepa_sctinst import Message
from faker import Faker

import pytest

fake = Faker()

schema_validation = SchemaValidation()
message_empty = 'Document is empty'

@pytest.mark.parametrize(
    "filename,message_type,is_valid,error_msg_present,expected_message",[
        ('tests/sct_inst_files/pacs008_valid.xml',Message.SCTINST, True, False,None), 
        ('tests/sct_inst_files/pacs008_invalid.xml',Message.SCTINST, False, True,None), 
        ('tests/sct_inst_files/pacs008_empty.xml',Message.SCTINST, False, True,message_empty),
        ('tests/sct_inst_files/pain001_valid.xml',Message.SCTINST_C2B, True, False,None)
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

