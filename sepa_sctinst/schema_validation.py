
from sepa_sctinst import MessageConfiguration
import lxml
from lxml import etree
import io

class SchemaValidation:
    """
    A class to validate SCTInst messages

    This object provide a schema validation method 

    """
    
    def validate(self,data:str,payment_conf:MessageConfiguration):
        """ XSD Validation for SCTInst messages
        where `data` is a XML message as string,
        `payment_conf` is an `sepa_sctinst.MessageConfiguration` wich provide the schema to use for validation
        
        Return: A `dict` with isValid key and error_messages key if isValid = False
        """

        with open(payment_conf.xsd_filepath) as f:
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



