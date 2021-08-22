from sepa_sctinst.sct_inst import SCTInst


class MessageConfiguration:
   def  __init__(self,code:str,xsd_filepath:str):
       """MessageConfiguration constructor

       Args:
           code (str): Payment code
           xsd_filepath (str): XSD file path
       """
       self.code = code
       self.xsd_filepath = xsd_filepath
        

class Message:
    """ All messages in the SCTInst scheme
    """
    SCTINST = MessageConfiguration(SCTInst,'sepa_sctinst/xsd/pacs.008.001.02.xsd')
    POSITIVE_STATUS = MessageConfiguration('PositiveStatus','sepa_sctinst/xsd/pacs.002.001.03_Positive_Update.xsd')
    NEGATIVE_STATUS = MessageConfiguration('NegativeStatus','sepa_sctinst/xsd/pacs.002.001.03_Negative.xsd')
    SCTINST_STATUS_INV = MessageConfiguration('SctinstStatusInv','sepa_sctinst/xsd/pacs.028.001.01_Status.xsd')
    
    RECALL = MessageConfiguration('Recall','sepa_sctinst/xsd/camt.056.001.01_Recall.xsd')
    RECALL_POS=MessageConfiguration('RecallPos','sepa_sctinst/xsd/pacs.004.001.02_PosAnRecall.xsd')
    RECALL_NEG=MessageConfiguration('RecallNeg','sepa_sctinst/xsd/camt.029.001.03_NegAnRecall.xsd')
    RECALL_STATUS_INV=MessageConfiguration('RecallStatusInv','sepa_sctinst/xsd/pacs.028.001.01_Recall_Update.xsd')
    
    RFRO = MessageConfiguration('RFRO','sepa_sctinst/xsd/pacs.008.001.02.xsd')
    RFRO_POS=MessageConfiguration('RfroPos','sepa_sctinst/xsd/pacs.004.001.02_PosReRFRO.xsd')
    RFRO_NEG=MessageConfiguration('RfroNeg','sepa_sctinst/xsd/camt.029.001.03_NegReRFRO.xsd')
    RFRO_STATUS_INV=MessageConfiguration('RfroStatusInv' ,'sepa_sctinst/xsd/pacs.028.001.01_RFRO_Update.xsd')
    
    SCTINST_C2B = MessageConfiguration('SCTInstC2B','sepa_sctinst/xsd/pain.001.001.03.xsd')
    SCTINST_C2B_BACK = MessageConfiguration('SCTInstBackC2B','sepa_sctinst/xsd/pain.001.001.03_TransferBack.xsd')
    SCTINST_C2B_STATUS = MessageConfiguration('SCTInstStatusC2B','sepa_sctinst/xsd/pain.002.001.03.xsd')