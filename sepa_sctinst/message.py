from faker import Faker
import re

class Message:
    """
    A class to describe message configuration.

    A message object provide all characteristics needed to validate a xml message.

    """
    
    code:str
    """Code is a mnemonic value for a specific message"""
    
    xsd_filepath:str
    """Relative path to the XSD file"""
    xmlns:str
    """XML namespace"""
    
    fn_msg_id:str
    """Message ID generator function"""
    
    fn_tx_id:str
    """Transaction ID generator function"""
    

    def  __init__(self,code:str,xsd_filepath:str,xmlns:str,fn_msg_id=None,fn_tx_id=None):
        """
        Initializes a message configuration
        """
        self.code = code
        self.xsd_filepath = xsd_filepath
        self.xmlns = xmlns
        self.fn_msg_id = fn_msg_id if fn_msg_id is not None else self.gen_message_id
        self.fn_tx_id = fn_tx_id if fn_msg_id is not None else self.gen_tx_id
    
    @staticmethod
    def gen_message_id():
        """
        Generate a message ID
        """
        fake = Faker()
        return fake.bothify(text='MSGID??????????????????????????????')
    
    @staticmethod
    def gen_tx_id():        
        """
        Generate a transaction ID
        """
        fake = Faker()
        return fake.bothify(text='TXID??????????????????????????????')
    

    @staticmethod
    def autodetect(data):
        """
        Return the :class:`sepa_sctinst.message.Message` object associated to the `data` parameter by matching with the xmlns attribute
        """
        from sepa_sctinst.default_messages import DefaultMessages
        xmlns = None
        xmlsn_regex = re.findall('xmlns=(".*?")',data)
       
        if len(xmlsn_regex) > 0:
            xmlns = xmlsn_regex[0].strip('"')
        for attr in dir(DefaultMessages):
            if type(getattr(DefaultMessages, attr)) == Message and getattr(DefaultMessages, attr).xmlns == xmlns:
                return getattr(DefaultMessages, attr)
                
        
