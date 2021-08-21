from sepa_sctinst.sct_inst import SCTInst


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
    SCTINST = PaymentConfiguration(SCTInst,'sepa_sctinst/xsd/pacs.008.001.02.xsd')
    POSITIVE_STATUS = PaymentConfiguration('PositiveStatus','sepa_sctinst/xsd/pacs.002.001.03_Positive_Update.xsd')
    NEGATIVE_STATUS = PaymentConfiguration('NegativeStatus','sepa_sctinst/xsd/pacs.002.001.03_Negative.xsd')
    SCTINST_STATUS_INV = PaymentConfiguration('SctinstStatusInv','sepa_sctinst/xsd/pacs.028.001.01_Status.xsd')
    
    RECALL = PaymentConfiguration('Recall','sepa_sctinst/xsd/camt.056.001.01_Recall.xsd')
    RECALL_POS=PaymentConfiguration('RecallPos','sepa_sctinst/xsd/pacs.004.001.02_PosAnRecall.xsd')
    RECALL_NEG=PaymentConfiguration('RecallNeg','sepa_sctinst/xsd/camt.029.001.03_NegAnRecall.xsd')
    RECALL_STATUS_INV=PaymentConfiguration('RecallStatusInv','sepa_sctinst/xsd/pacs.028.001.01_Recall_Update.xsd')
    
    RFRO = PaymentConfiguration('RFRO','sepa_sctinst/xsd/pacs.008.001.02.xsd')
    RFRO_POS=PaymentConfiguration('RfroPos','sepa_sctinst/xsd/pacs.004.001.02_PosReRFRO.xsd')
    RFRO_NEG=PaymentConfiguration('RfroNeg','sepa_sctinst/xsd/camt.029.001.03_NegReRFRO.xsd')
    RFRO_STATUS_INV=PaymentConfiguration('RfroStatusInv' ,'sepa_sctinst/xsd/pacs.028.001.01_RFRO_Update.xsd') 