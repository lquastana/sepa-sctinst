import pytest

from sepa_sctinst.schema_validation import SchemaValidation
from sepa_sctinst import Payment

schema_validation = SchemaValidation()

message_empty = 'Document is empty'


@pytest.mark.parametrize(
    "filename,message_type,is_valid,error_msg_present,expected_message",[
        ('sepa_sctinst/test/sct_inst_files/pacs008_valid.xml',Payment.SCTINST, True, False,None), 
        ('sepa_sctinst/test/sct_inst_files/pacs008_invalid.xml',Payment.SCTINST, False, True,None), 
        ('sepa_sctinst/test/sct_inst_files/pacs008_empty.xml',Payment.SCTINST, False, True,message_empty)
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
    