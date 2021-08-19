
import lxml
from lxml import etree
import io

"""
    XSD validation for 008.001.02 message
    Parameters
    ----------
    data : str, default None
        Payment message as string
"""
def validate(data):

    with open('sctinst/xsd/pacs.008.001.02.xsd') as f:
        schema_root = f.read()
    
    schemaDoc = etree.parse(io.BytesIO(schema_root.encode('utf-8')))
    schema = etree.XMLSchema(schemaDoc)

    parser = etree.XMLParser(schema = schema)
    try:
        lxml.etree.fromstring(data.encode('utf-8'), parser)
        return {'isValid':True}
    except lxml.etree.XMLSyntaxError as e:
        print(e)
        return {
            'isValid':False,
            'error_message': e
        }



