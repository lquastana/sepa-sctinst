
import lxml
from lxml import etree
import io

PAYMENT_TYPES = {
    'SCTInst':'sctinst/xsd/pacs.008.001.02.xsd',
    'Negative':'sctinst/xsd/pacs.002.001.03_Negative.xsd'
}

class SchemaValidation:
    def __init__(self, payment_types=PAYMENT_TYPES):
        self.payments_types = payment_types


    """
        XSD validation for 008.001.02 message
        Parameters
        ----------
        data : str, default None
            Payment message as string
        message_type : str, default None
            Type of Payment
    """
    def validate(self,data,payment_type):

        if (payment_type not in self.payments_types) :
            return {
                'isValid':False,
                'error_messages': ['Message type not found.']
            }

        with open(self.payments_types[payment_type]) as f:
            schema_root = f.read()
        
        schema_doc = etree.parse(io.BytesIO(schema_root.encode('utf-8')))
        schema = etree.XMLSchema(schema_doc)

        parser = etree.XMLParser(schema = schema)
        try:
            lxml.etree.fromstring(data.encode('utf-8'), parser)
            return {'isValid':True}
        except lxml.etree.XMLSyntaxError as err:
            return {
                'isValid':False,
                'error_messages': list(err.args)
            }



