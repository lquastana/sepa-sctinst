
from sepa_sctinst import PaymentConfiguration
import lxml
from lxml import etree
import io



class SchemaValidation:
    def validate(self,data:str,payment_conf:PaymentConfiguration):
        """ XSD Validation for SCTInst payment

        Args:
            data (str): XML Data
            payment_conf (PaymentConfiguration): Payment configuration

        Returns:
            dict: Dict with isValid and error_messages if isValid = False
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



