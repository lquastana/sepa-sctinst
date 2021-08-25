from sepa_sctinst.sct_inst_common import Participant
import xml.etree.ElementTree as ET
from datetime import datetime,date
import random
from faker import Faker

SERVICE_LEVEL_CODE = 'SEPA'
LOCAL_INSTRUMENT = 'INST'
CHARGE_BEARER='SLEV'
CURRENCY='EUR'

class GroupHeader:
    """A class to represent the group header in interbank SCTInst message
    
    Set of characteristics shared by all individual transactions included in the message.
    """
    
    message_identification:str
    """Message Identification assigned by the
instructing party, and sent to the next party in the
chain to unambiguously identify the message."""
    creation_datetime:datetime
    """Date and time at which the message was created."""
    interbank_sttlmt_date:date
    """Date on which the amount of money ceases to be
available to the agent that owes it and when the
amount of money becomes available to the agent
to which it is due."""
    sttlmt_method:str
    """Method used to settle the (batch of) payment
instructions.Only CLRG, INGA and INDA are allowed"""
        
    def __init__(self,
                 message_identification:str,
                 creation_datetime:datetime,
                 interbank_sttlmt_date:date,
                 sttlmt_method:str
                 ):
        """Initializes a group header object
        """
        self.message_identification = message_identification
        self.creation_datetime = creation_datetime
        self.interbank_sttlmt_date = interbank_sttlmt_date
        self.sttlmt_method = sttlmt_method


class Transaction:
    """A class to represent a transaction in interbank SCTInst message
    
    """
    
    beneficiary:Participant
    """Beneficiary informations as `sepa_sctinst.sct_inst.Participant`"""
    amount:float
    """The amount of the SCT Inst in Euro """
    end_to_end_id:str
    """Original End To End Identification. Unique identification, as assigned by the original
initiating party """    
    tx_id:str
    """Original Transaction Identification. Unique identification, as assigned by the original
first instructing agent """
    acceptance_datetime:datetime
    """Point in time when the payment order from the
initiating party meets the processing conditions of
the account servicing agent."""
    reference:str
    """Reference information provided by the creditor to
allow the identification of the underlying
documents."""
    remittance_information:str
    """Remittance information"""
    
    def __init__(self,beneficiary:Participant,amount:float,end_to_end_id:str,tx_id:str,acceptance_datetime:datetime,reference:str,remittance_information:str):
        """Initializes a transaction object
        """ 
        self.beneficiary = beneficiary
        self.amount = amount
        self.tx_id = tx_id
        self.end_to_end_id = end_to_end_id
        self.acceptance_datetime = acceptance_datetime
        self.reference = reference
        self.remittance_information = remittance_information,

class SCTInst:
    """A class to represent a SCTInst interbank message
    """
    group_header:GroupHeader
    """`sepa_sctinst.sct_inst.GroupHeader` object shared by all individual transactions included in the message. """
    originator:Participant
    """Originator `sepa_sctinst.sct_inst.Participant` object that initiates the payment. """
    transaction:Transaction
    """`sepa_sctinst.sct_inst.Transaction` object give information about the transaction. """

    def __init__(self,group_header:GroupHeader,originator:Participant,transaction:Transaction):
        """Initializes a SCTInst object
        """ 
        self.group_header = group_header
        self.originator = originator
        self.transaction = transaction

    @staticmethod
    def random():
        """Generate random SCTInst object

        Returns `sepa_sctinst.sct_inst.SCTInst` object with random value
        """
        fake = Faker()
        
        group_header = GroupHeader(fake.bothify(text='MSGID?????????'),fake.date_time(),fake.date_object(),'CLRG')
        originator = Participant(fake.lexify(text='????',letters='ABCDEFGRHIJKL') + fake.bank_country() + 'PPXXX',
                                 fake.iban(),fake.name())
        beneficiary = Participant(fake.lexify(text='????',letters='ABCDEFGRHIJKL') + fake.bank_country() + 'PPXXX',
                                  fake.iban(),fake.name())
        transation = Transaction(beneficiary,
                                 str(round(random.uniform(1,2), 2)),
                                 fake.bothify(text='ENDTOEND?????????'),
                                 fake.bothify(text='TXID?????????'),
                                 fake.date_time(),
                                 fake.bothify(text='REF?????????'),
                                 fake.bothify(text='REMINF?????????'))
    
        return SCTInst(group_header,originator,transation)
        
    

    def to_xml(self):
        """ Generate message as XML Document
        Returns a string as XML dcoument
        """
        
        root = ET.Element("Document")
        root.set('xmlns',"urn:iso:std:iso:20022:tech:xsd:pacs.008.001.02")
        root_fito = ET.SubElement(root, "FIToFICstmrCdtTrf")
        
        self.xml_header(root_fito)
        self.xml_transaction(root_fito)

        ET.ElementTree(root)
 
        return ET.tostring(root,encoding='utf-8',xml_declaration=True).decode('utf-8')

    def xml_transaction(self, root_fito):
        cdt_tx = ET.SubElement(root_fito, "CdtTrfTxInf")
        cdt_tx_pmt = ET.SubElement(cdt_tx, "PmtId")
            
        cdt_tx_pmt_e2e = ET.SubElement(cdt_tx_pmt, "EndToEndId")
        cdt_tx_pmt_e2e.text = self.transaction.end_to_end_id
            
        cdt_tx_pmt_id = ET.SubElement(cdt_tx_pmt, "TxId")
        cdt_tx_pmt_id.text = self.transaction.tx_id
            
        cdt_tx_pmt_amt = ET.SubElement(cdt_tx, "IntrBkSttlmAmt")
        cdt_tx_pmt_amt.set('Ccy',CURRENCY)
        cdt_tx_pmt_amt.text = str(self.transaction.amount)
        
            
        cdt_tx_pmt_acceptance_datetime = ET.SubElement(cdt_tx, "AccptncDtTm")
        cdt_tx_pmt_acceptance_datetime.text = self.transaction.acceptance_datetime.isoformat()
            
        cdt_tx_pmt_chrbr = ET.SubElement(cdt_tx, "ChrgBr")
        cdt_tx_pmt_chrbr.text = CHARGE_BEARER
        
        Participant.to_xml(self,cdt_tx,self.transaction,'Dbtr')
        Participant.to_xml(self,cdt_tx,self.transaction,'Cdtr')
        


    def xml_header(self, root_fito):
        grp_header = ET.SubElement(root_fito, "GrpHdr")
        
        header_id = ET.SubElement(grp_header, "MsgId")
        header_id.text = str(self.group_header.message_identification)
        
        header_cre_dt_tm = ET.SubElement(grp_header, "CreDtTm")
        header_cre_dt_tm.text = self.group_header.creation_datetime.isoformat()
        
        header_nb_txs = ET.SubElement(grp_header, "NbOfTxs")
        header_nb_txs.text = '1'
        
        header_tt_amount = ET.SubElement(grp_header, "TtlIntrBkSttlmAmt")
        header_tt_amount.set('Ccy','EUR')
        header_tt_amount.text = str(self.transaction.amount)
        
        header_sttlm_dt = ET.SubElement(grp_header, "IntrBkSttlmDt")
        header_sttlm_dt.text = self.group_header.interbank_sttlmt_date.isoformat()
        
        header_sttlm = ET.SubElement(grp_header, "SttlmInf")
        header_sttlm_mdt = ET.SubElement(header_sttlm, "SttlmMtd")
        header_sttlm_mdt.text = self.group_header.sttlmt_method
        
        header_pmt_tp = ET.SubElement(grp_header, "PmtTpInf")
        
        header_pmt_tp_svc = ET.SubElement(header_pmt_tp, "SvcLvl")
        header_pmt_tp_svc_cd = ET.SubElement(header_pmt_tp_svc, "Cd")
        header_pmt_tp_svc_cd.text = SERVICE_LEVEL_CODE
        
        header_pmt_tp_lcl_inst = ET.SubElement(header_pmt_tp, "LclInstrm")
        header_pmt_tp_lcl_inst_cd = ET.SubElement(header_pmt_tp_lcl_inst, "Cd")
        header_pmt_tp_lcl_inst_cd.text = LOCAL_INSTRUMENT


