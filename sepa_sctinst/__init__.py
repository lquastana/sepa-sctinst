from sepa_sctinst.sct_inst_interbank import SCTInst
from sepa_sctinst.sct_inst_c2b import SCTInstC2B
from lxml import etree as ET
import re

class MessageConfiguration:
    """
    A class to describe message configuration.

    A message configuration object provide all characteristics needed to validate a xml message.

    """
    
    code:str
    """Code is a mnemonic value for a specific message"""
    
    xsd_filepath:str
    """Relative path to the XSD file"""
    xmlns:str
    """XML namespace"""
    
    def  __init__(self,code:str,xsd_filepath:str,xmlns:str):
        """
        Initializes a message configuration
        """
        self.code = code
        self.xsd_filepath = xsd_filepath
        self.xmlns = xmlns

    @staticmethod
    def autodetect(data):
        """
        Return the `sepa_sctinst.MessageConfiguration` object associated to the `data` parameter by matching with the xmlns attribute
        """
        xmlns = None
        xmlsn_regex = re.findall('xmlns=(".*?")',data)
       
        if len(xmlsn_regex) > 0:
            xmlns = xmlsn_regex[0].strip('"')
        for attr in dir(Message):
            if type(getattr(Message, attr)) == MessageConfiguration and getattr(Message, attr).xmlns == xmlns:
                return getattr(Message, attr)
                
        

class Message:
    """ 
    All `sepa_sctinst.MessageConfiguration` objects available on the SCTInst scheme (Interbank and C2B)
    """
    SCTINST = MessageConfiguration(SCTInst,
                                   'sepa_sctinst/xsd/pacs.008.001.02.xsd',
                                   'urn:iso:std:iso:20022:tech:xsd:pacs.008.001.02')
    POSITIVE_STATUS = MessageConfiguration('PositiveStatus',
                                           'sepa_sctinst/xsd/pacs.002.001.03_Positive_Update.xsd',
                                           'urn:iso:std:iso:20022:tech:xsd:pacs.002.001.03')
    NEGATIVE_STATUS = MessageConfiguration('NegativeStatus',
                                           'sepa_sctinst/xsd/pacs.002.001.03_Negative.xsd',
                                           'urn:iso:std:iso:20022:tech:xsd:pacs.002.001.03')
    SCTINST_STATUS_INV = MessageConfiguration('SctinstStatusInv',
                                              'sepa_sctinst/xsd/pacs.028.001.01_Status.xsd',
                                              'urn:iso:std:iso:20022:tech:xsd:pacs.028.001.01')
    
    RECALL = MessageConfiguration('Recall',
                                  'sepa_sctinst/xsd/camt.056.001.01_Recall.xsd',
                                  'urn:iso:std:iso:20022:tech:xsd:camt.056.001.01')
    RECALL_POS=MessageConfiguration('RecallPos',
                                    'sepa_sctinst/xsd/pacs.004.001.02_PosAnRecall.xsd',
                                    'urn:iso:std:iso:20022:tech:xsd:pacs.004.001.02')
    RECALL_NEG=MessageConfiguration('RecallNeg',
                                    'sepa_sctinst/xsd/camt.029.001.03_NegAnRecall.xsd',
                                    'urn:iso:std:iso:20022:tech:xsd:camt.029.001.03')
    RECALL_STATUS_INV=MessageConfiguration('RecallStatusInv',
                                           'sepa_sctinst/xsd/pacs.028.001.01_Recall_Update.xsd',
                                           'urn:iso:std:iso:20022:tech:xsd:028.001.01')
    
    RFRO = MessageConfiguration('RFRO',
                                'sepa_sctinst/xsd/camt.056.001.01_RFRO.xsd',
                                'urn:iso:std:iso:20022:tech:xsd:camt.056.001.01')
    RFRO_POS=MessageConfiguration('RfroPos',
                                  'sepa_sctinst/xsd/pacs.004.001.02_PosReRFRO.xsd',
                                  'urn:iso:std:iso:20022:tech:xsd:pacs.004.001.02')
    RFRO_NEG=MessageConfiguration('RfroNeg',
                                  'sepa_sctinst/xsd/camt.029.001.03_NegReRFRO.xsd',
                                  'urn:iso:std:iso:20022:tech:xsd:camt.029.001.03')
    RFRO_STATUS_INV=MessageConfiguration('RfroStatusInv' ,
                                         'sepa_sctinst/xsd/pacs.028.001.01_RFRO_Update.xsd',
                                         'urn:iso:std:iso:20022:tech:xsd:pacs.028.001.01')
    
    SCTINST_C2B = MessageConfiguration(SCTInstC2B,
                                       'sepa_sctinst/xsd/pain.001.001.03.xsd',
                                       'urn:iso:std:iso:20022:tech:xsd:pain.001.001.03')
    SCTINST_C2B_BACK = MessageConfiguration('SCTInstBackC2B',
                                            'sepa_sctinst/xsd/pain.001.001.03_TransferBack.xsd',
                                            'urn:iso:std:iso:20022:tech:xsd:pain.001.001.03')
    SCTINST_C2B_STATUS = MessageConfiguration('SCTInstStatusC2B',
                                              'sepa_sctinst/xsd/pain.002.001.03.xsd',
                                              'urn:iso:std:iso:20022:tech:xsd:pain.002.001.03')