
from sepa_sctinst.message import Message
import lxml
from lxml import etree
import io

class SchemaValidation:
    """
    A class to validate SCTInst messages

    This object provide a schema validation method 

    """
    
    @staticmethod
    def validate(data:str,message:Message):
        """ XSD Validation for SCTInst messages
        where `data` is a XML message as string,
        `message` is an :class:`sepa_sctinst.message.Message` wich provide the schema to use for validation
        
        Return: A `dict` with isValid key and error_messages key if isValid = False
        """

        with open(message.xsd_filepath) as f:
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



