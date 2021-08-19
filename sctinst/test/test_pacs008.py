import pytest
from sctinst.scheme.pacs008 import validate

@pytest.mark.parametrize(
    "filename,is_valid,error_msg_present",[
        ('sctinst/test/pacs008_files/pacs008_valid.xml', True, False), 
        ('sctinst/test/pacs008_files/pacs008_invalid.xml', False, True), 
        ('sctinst/test/pacs008_files/pacs008_empty.xml', False, True), 
    ]
)
def test_pacs008_xsd(filename,is_valid,error_msg_present):

    with open(filename, 'r') as input:
        data = input.read()
    response = validate(data)

    assert response['isValid'] == is_valid
    assert ('message' in response) == error_msg_present