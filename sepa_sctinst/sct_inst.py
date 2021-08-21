import xml.etree.ElementTree as ET
from datetime import datetime,date
import functools
import random
from faker import Faker

SERVICE_LEVEL_CODE = 'SEPA'
LOCAL_INSTRUMENT = 'INST'
CHARGE_BEARER='SLEV'
CURRENCY='EUR'

class GroupHeader:
    
    def __init__(self,
                 message_identification:str,
                 creation_datetime:datetime,
                 interbank_sttlmt_date:date,
                 sttlmt_method:str
                 ):
        """GroupHeader constructor

        Args:
            message_identification (str): Message Identification
            creation_datetime (datetime): Creation Date Time
            interbank_sttlmt_date (date): Interbank Settlement Date
            sttlmt_method (str): Settlement Method
        """
        self.message_identification = message_identification
        self.creation_datetime = creation_datetime
        self.interbank_sttlmt_date = interbank_sttlmt_date
        self.sttlmt_method = sttlmt_method

class Participant:
    def __init__(self,bic,iban,name):
        """ Participant constructor

        Args:
            bic (str): OPTIONAL Business Identifier Code
            iban (str): International Bank Account Number of the creditor
            name (str): Name of the initiating party and creditor
        """        
        self.bic = bic
        self.iban = iban
        self.name = name

class Transaction:
    def __init__(self,beneficiary:Participant,amount:float,end_to_end_id:str,tx_id:str,acceptance_datetime:datetime,reference:str,remittance_information:str):
        """[summary]

        Args:
            beneficiary (Participant): Beneficiary informations
            amount (float): Amount
            end_to_end_id (str): End To End Identification
            tx_id (str): Transaction Identification
            acceptance_datetime (datetime): Acceptance Date Time
            reference (str): Reference
            remittance_information (str): Remittance information
        """
        
        self.beneficiary = beneficiary
        self.amount = amount
        self.tx_id = tx_id
        self.end_to_end_id = end_to_end_id
        self.acceptance_datetime = acceptance_datetime
        self.reference = reference
        self.remittance_information = remittance_information,

class SCTInst:
    
    group_header:GroupHeader
    originator:Participant
    transaction:Transaction

    def __init__(self,group_header:GroupHeader,originator:Participant,transaction:Transaction):
        """SCTInst constructor

        Args:
            group_header (GroupHeader): Group Header
            originator (Participant): Originator informations
            transaction (Transaction): Transaction informations
        """
        self.group_header = group_header
        self.originator = originator
        self.transaction = transaction

    @staticmethod
    def random():
        """Generate random SCTInst object

        Returns:
            SCTInst: SCTInst object with random value
        """
        fake = Faker()
        
        group_header = GroupHeader(fake.bothify(text='MSGID?????????'),fake.date_time(),fake.date_object(),'CLRG')
        originator = Participant(fake.swift(),fake.iban(),fake.name())
        
        beneficiary = Participant(fake.swift(),fake.iban(),fake.name())
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

        Returns:
            str: XML dcoument
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
        
        self.xml_party_inf(cdt_tx,self.transaction,'Dbtr')
        self.xml_party_inf(cdt_tx,self.transaction,'Cdtr')
        
        
    def xml_party_inf(self, transaction_node:ET.SubElement,transaction:Transaction, stakeholder:str):
        stakeholder_node = ET.Element(stakeholder)
        stakeholder_name = ET.SubElement(stakeholder_node, 'Nm')
        if stakeholder == 'Dbtr':
            stakeholder_name.text = self.originator.name
        else:
            stakeholder_name.text = transaction.beneficiary.name
        
        stakeholder_acct = ET.Element(stakeholder+'Acct')
        stakeholder_acct_id = ET.SubElement(stakeholder_acct, 'Id')
        stakeholder_acct_iban = ET.SubElement(stakeholder_acct_id, 'IBAN')
        if stakeholder == 'Dbtr':
            stakeholder_acct_iban.text = self.originator.iban
        else:
            stakeholder_acct_iban.text = transaction.beneficiary.iban
        
        stakeholder_agt = ET.Element(stakeholder+'Agt')
        stakeholder_agt_fin_inst = ET.SubElement(stakeholder_agt, 'FinInstnId')
        stakeholder_agt_fin_inst_bic = ET.SubElement(stakeholder_agt_fin_inst, 'BIC')
        if stakeholder == 'Dbtr':
            stakeholder_agt_fin_inst_bic.text = self.originator.bic
        else:
            stakeholder_agt_fin_inst_bic.text = transaction.beneficiary.bic
        
        if stakeholder == 'Dbtr':
            transaction_node.append(stakeholder_node)
            transaction_node.append(stakeholder_acct)
            transaction_node.append(stakeholder_agt)
        else:
            transaction_node.append(stakeholder_agt)
            transaction_node.append(stakeholder_node)
            transaction_node.append(stakeholder_acct)
               
            
            


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


