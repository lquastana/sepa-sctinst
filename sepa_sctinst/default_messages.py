from sepa_sctinst.message import Message

class DefaultMessages:
    '''All :class:`sepa_sctinst.message.Message` objects available on the SCTInst scheme (Interbank and C2B)
    '''
    SCTINST_INTERBANK = Message('SCTInst',
                    'sepa_sctinst/xsd/pacs.008.001.02.xsd',
                    'urn:iso:std:iso:20022:tech:xsd:pacs.008.001.02')

    POSITIVE_STATUS = Message('PositiveStatus',
                            'sepa_sctinst/xsd/pacs.002.001.03_Positive_Update.xsd',
                            'urn:iso:std:iso:20022:tech:xsd:pacs.002.001.03')

    NEGATIVE_STATUS = Message('NegativeStatus',
                            'sepa_sctinst/xsd/pacs.002.001.03_Negative.xsd',
                            'urn:iso:std:iso:20022:tech:xsd:pacs.002.001.03')

    SCTINST_STATUS_INV = Message('SctinstStatusInv',
                                'sepa_sctinst/xsd/pacs.028.001.01_Status.xsd',
                                'urn:iso:std:iso:20022:tech:xsd:pacs.028.001.01')
        
    RECALL = Message('Recall',
                    'sepa_sctinst/xsd/camt.056.001.01_Recall.xsd',
                    'urn:iso:std:iso:20022:tech:xsd:camt.056.001.01')

    RECALL_POS=Message('RecallPos',
                    'sepa_sctinst/xsd/pacs.004.001.02_PosAnRecall.xsd',
                    'urn:iso:std:iso:20022:tech:xsd:pacs.004.001.02')

    RECALL_NEG=Message('RecallNeg',
                    'sepa_sctinst/xsd/camt.029.001.03_NegAnRecall.xsd',
                    'urn:iso:std:iso:20022:tech:xsd:camt.029.001.03')

    RECALL_STATUS_INV=Message('RecallStatusInv',
                            'sepa_sctinst/xsd/pacs.028.001.01_Recall_Update.xsd',
                            'urn:iso:std:iso:20022:tech:xsd:028.001.01')
        
    RFRO = Message('RFRO',
                'sepa_sctinst/xsd/camt.056.001.01_RFRO.xsd',
                'urn:iso:std:iso:20022:tech:xsd:camt.056.001.01')

    RFRO_POS=Message('RfroPos',
                    'sepa_sctinst/xsd/pacs.004.001.02_PosReRFRO.xsd',
                    'urn:iso:std:iso:20022:tech:xsd:pacs.004.001.02')

    RFRO_NEG=Message('RfroNeg',
                    'sepa_sctinst/xsd/camt.029.001.03_NegReRFRO.xsd',
                    'urn:iso:std:iso:20022:tech:xsd:camt.029.001.03')

    RFRO_STATUS_INV=Message('RfroStatusInv' ,
                            'sepa_sctinst/xsd/pacs.028.001.01_RFRO_Update.xsd',
                            'urn:iso:std:iso:20022:tech:xsd:pacs.028.001.01')
        
    SCTINST_C2B = Message('SCTInstC2B',
                        'sepa_sctinst/xsd/pain.001.001.03.xsd',
                        'urn:iso:std:iso:20022:tech:xsd:pain.001.001.03')

    SCTINST_C2B_BACK = Message('SCTInstBackC2B',
                            'sepa_sctinst/xsd/pain.001.001.03_TransferBack.xsd',
                            'urn:iso:std:iso:20022:tech:xsd:pain.001.001.03')

    SCTINST_C2B_STATUS = Message('SCTInstStatusC2B',
                                'sepa_sctinst/xsd/pain.002.001.03.xsd',
                                'urn:iso:std:iso:20022:tech:xsd:pain.002.001.03')