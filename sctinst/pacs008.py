
import io
import xml.etree.ElementTree as ET
from datetime import datetime,date
import functools

class IbanData:
    def __init__(self,bic,iban,name):
        """ IbanData constructor

        Args:
            bic (str): OPTIONAL Business Identifier Code
            iban (str): International Bank Account Number of the creditor
            name (str): Name of the initiating party and creditor
        """        
        self.bic = bic
        self.iban = iban
        self.name = name

class Transaction:
    def __init__(self,name,bic,iban,amount,instruction,reference,remittance_information,requested_date,currency='EUR'):
        """ Transaction construction

        Args:
            name (str): Name of the creditor
            bic (str): OPTIONAL Business Identifier Code
            iban (str): International Bank Account Number of the creditors account
            amount (str): Amount
            instruction (str): OPTIONAL Instruction Identification
            reference (str): OPTIONAL End-To-End-Identification
            remittance_information (str): OPTIONAL Unstructured remittance information
            requested_date (date): OPTIONAL Requested execution date
            currency (str, optional): OPTIONAL Currency EUR by default
        """        
        self.name = name
        self.bic = bic
        self.iban = iban
        self.amount = amount
        self.instruction = instruction
        self.reference = reference
        self.remittance_information = remittance_information,
        self.requested_date = requested_date,
        self.currency = currency

class SCTInst:

    transactions:list = [Transaction]
    message_identification:str
    initiating_party_name:str
    debtor:IbanData
    

    def __init__(self, message_identification,initiating_party_name,debtor:IbanData):
        """[summary]

        Args:
            message_identification ([type]): [description]
            initiating_party_name ([type]): [description]
            debtor (IbanData): [description]
        """
    
        self.message_identification = message_identification
        self.initiating_party_name = initiating_party_name
        self.debtor = debtor
        self.transactions = []  

    def add_transaction(self,transaction:Transaction):
        """ Add transaction

        Args:
            transaction (Transaction): Transaction
        """
        self.transactions.append(transaction)
    

    def to_xml(self):
        """ Generate message as XML Document

        Returns:
            str: XML dcoument
        """
        
        if len(self.transactions) == 0:
            raise ValueError('You need a minimum of 1 transaction')
        
        root = ET.Element("Document")
        root.set('xmlns',"urn:iso:std:iso:20022:tech:xsd:pacs.008.001.02")
        root_fito = ET.SubElement(root, "FIToFICstmrCdtTrf")
        self.xml_header(root_fito)
        
        for transaction in self.transactions:
            self.xml_transaction(root_fito, transaction)

        ET.ElementTree(root)
 
        return ET.tostring(root,encoding='utf-8',xml_declaration=True).decode('utf-8')

    def xml_transaction(self, root_fito, transaction):
        cdt_tx = ET.SubElement(root_fito, "CdtTrfTxInf")
        cdt_tx_pmt = ET.SubElement(cdt_tx, "PmtId")
            
        cdt_tx_pmt_e2e = ET.SubElement(cdt_tx_pmt, "EndToEndId")
        cdt_tx_pmt_e2e.text = 'E2E ID'
            
        cdt_tx_pmt_id = ET.SubElement(cdt_tx_pmt, "TxId")
        cdt_tx_pmt_id.text = 'TX ID'
            
        cdt_tx_pmt_amt = ET.SubElement(cdt_tx, "IntrBkSttlmAmt")
        cdt_tx_pmt_amt.set('Ccy','EUR')
        cdt_tx_pmt_amt.text = str(transaction.amount)
        
            
        cdt_tx_pmt_accptnc_dtm = ET.SubElement(cdt_tx, "AccptncDtTm")
        cdt_tx_pmt_accptnc_dtm.text = datetime.today().isoformat()
            
        cdt_tx_pmt_chrbr = ET.SubElement(cdt_tx, "ChrgBr")
        cdt_tx_pmt_chrbr.text = 'SLEV'
        
        self.xml_party_inf(cdt_tx,transaction,'Dbtr')
        self.xml_party_inf(cdt_tx,transaction,'Cdtr')
        
        
    def xml_party_inf(self, transaction_node:ET.SubElement,transaction:Transaction, stakeholder:str):
        stakeholder_node = ET.Element(stakeholder)
        stakeholder_name = ET.SubElement(stakeholder_node, 'Nm')
        if stakeholder == 'Dbtr':
            stakeholder_name.text = self.debtor.name
        else:
            stakeholder_name.text = transaction.name
        
        stakeholder_acct = ET.Element(stakeholder+'Acct')
        stakeholder_acct_id = ET.SubElement(stakeholder_acct, 'Id')
        stakeholder_acct_iban = ET.SubElement(stakeholder_acct_id, 'IBAN')
        if stakeholder == 'Dbtr':
            stakeholder_acct_iban.text = self.debtor.iban
        else:
            stakeholder_acct_iban.text = transaction.iban
        
        stakeholder_agt = ET.Element(stakeholder+'Agt')
        stakeholder_agt_fin_inst = ET.SubElement(stakeholder_agt, 'FinInstnId')
        stakeholder_agt_fin_inst_bic = ET.SubElement(stakeholder_agt_fin_inst, 'BIC')
        if stakeholder == 'Dbtr':
            stakeholder_agt_fin_inst_bic.text = self.debtor.bic
        else:
            stakeholder_agt_fin_inst_bic.text = transaction.bic
        
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
        print(self.message_identification)
        header_id.text = str(self.message_identification)
        
        header_cre_dt_tm = ET.SubElement(grp_header, "CreDtTm")
        header_cre_dt_tm.text = datetime.today().isoformat()
        
        header_nb_txs = ET.SubElement(grp_header, "NbOfTxs")
        header_nb_txs.text = str(len(self.transactions))
        
        header_tt_amount = ET.SubElement(grp_header, "TtlIntrBkSttlmAmt")
        header_tt_amount.set('Ccy','EUR')
        if len(self.transactions)>1 :
            header_tt_amount.text = str(functools.reduce(lambda a, b: a.amount+b.amount, self.transactions))
        elif len(self.transactions)== 1 :
            header_tt_amount.text = str(self.transactions[0].amount)
        else:
            header_tt_amount.text = '0'
        
        header_sttlm_dt = ET.SubElement(grp_header, "IntrBkSttlmDt")
        header_sttlm_dt.text = date.today().isoformat()
        
        header_sttlm = ET.SubElement(grp_header, "SttlmInf")
        header_sttlm_mdt = ET.SubElement(header_sttlm, "SttlmMtd")
        header_sttlm_mdt.text = 'CLRG'
        
        header_pmt_tp = ET.SubElement(grp_header, "PmtTpInf")
        
        header_pmt_tp_svc = ET.SubElement(header_pmt_tp, "SvcLvl")
        header_pmt_tp_svc_cd = ET.SubElement(header_pmt_tp_svc, "Cd")
        header_pmt_tp_svc_cd.text = 'SEPA'
        
        header_pmt_tp_lcl_inst = ET.SubElement(header_pmt_tp, "LclInstrm")
        header_pmt_tp_lcl_inst_cd = ET.SubElement(header_pmt_tp_lcl_inst, "Cd")
        header_pmt_tp_lcl_inst_cd.text = 'INST'


