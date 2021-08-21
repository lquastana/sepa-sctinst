from sctinst.pacs008 import SCTInst


class PaymentConfiguration:
   def  __init__(self,code:str,xsd_filepath:str):
       """PaymentConfiguration constructor

       Args:
           code (str): Payment code
           xsd_filepath (str): XSD file path
       """
       self.code = code
       self.xsd_filepath = xsd_filepath
        

class Payment:
    """ All type of payments in the SCTInst scheme
    """
    SCTINST = PaymentConfiguration(SCTInst,'sctinst/xsd/pacs.008.001.02.xsd')
    POSITIVE_STATUS = PaymentConfiguration('PositiveStatus','sctinst/xsd/pacs.002.001.03_Positive_Update.xsd')
    NEGATIVE_STATUS = PaymentConfiguration('NegativeStatus','sctinst/xsd/pacs.002.001.03_Negative.xsd')
    SCTINST_STATUS_INV = PaymentConfiguration('SctinstStatusInv','sctinst/xsd/pacs.028.001.01_Status.xsd')
    
    RECALL = PaymentConfiguration('Recall','sctinst/xsd/camt.056.001.01_Recall.xsd')
    RECALL_POS=PaymentConfiguration('RecallPos','sctinst/xsd/pacs.004.001.02_PosAnRecall.xsd')
    RECALL_NEG=PaymentConfiguration('RecallNeg','sctinst/xsd/camt.029.001.03_NegAnRecall.xsd')
    RECALL_STATUS_INV=PaymentConfiguration('RecallStatusInv','sctinst/xsd/pacs.028.001.01_Recall_Update.xsd')
    
    RFRO = PaymentConfiguration('RFRO','sctinst/xsd/pacs.008.001.02.xsd')
    RFRO_POS=PaymentConfiguration('RfroPos','sctinst/xsd/pacs.004.001.02_PosReRFRO.xsd')
    RFRO_NEG=PaymentConfiguration('RfroNeg','sctinst/xsd/camt.029.001.03_NegReRFRO.xsd')
    RFRO_STATUS_INV=PaymentConfiguration('RfroStatusInv' ,'sctinst/xsd/pacs.028.001.01_RFRO_Update.xsd') 