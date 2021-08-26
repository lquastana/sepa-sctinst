from sepa_sctinst.sct_inst_common import Participant
import xml.etree.ElementTree as ET
from datetime import datetime,date
import functools
import random
from faker import Faker

PAYMENT_METHOD='TRF'
CURRENCY='EUR'
SERVICE_LEVEL='SEPA'
CHARGE_BEARER='SLEV'

class GroupHeader:
    """A class to represent a group header in C2B SCTInst message  
    Set of characteristics shared by all individual transactions included in the message.
    """
    
    message_identification:str
    """Message Identification assigned by the
instructing party, and sent to the next party in the
chain to unambiguously identify the message."""
    creation_datetime:datetime
    """Date and time at which the message was created."""
    
    init_party_name:str
    """Name by which a party is known and which is
usually used to identify that party."""
    
    
    def __init__(self,
                 message_identification:str,
                 creation_datetime:datetime,
                 init_party_name:str
                 ):

        self.message_identification = message_identification
        self.creation_datetime = creation_datetime
        self.init_party_name = init_party_name
        
        
class PaymentInformation:
    """A class to represent a payment information in C2B SCTInst message
    """
    
    payment_id:str
    """Unique identification, as assigned by a sending
party, to unambiguously identify the payment
information group within the message."""
    batch_booking:bool
    """Identifies whether a single entry per individual
transaction or a batch entry for the sum of the
amounts of all transactions within the group of a
message is requested."""
    
    requ_exe_date:date
    """Date at which the initiating party requests the
clearing agent to process the payment. """
    
    def __init__(self,
                 payment_id:str,
                 batch_booking:bool,
                 requ_exe_date:date,
                 ):
        """Initializes a payment information object
        """
        self.payment_id = payment_id
        self.batch_booking = batch_booking
        self.requ_exe_date = requ_exe_date

class Transaction:
    """A class to represent a transaction in C2B SCTInst message
    
    """
    
    beneficiary:Participant
    """Beneficiary informations as `sepa_sctinst.sct_inst_c2b.Participant`"""
    amount:float
    """The amount of the SCT Inst in Euro """
    end_to_end_id:str
    """Unique identification assigned by the initiating
party to unumbiguously identify the transaction."""   
    remittance_information:str
    """Information supplied to enable the matching of
an entry with the items that the transfer is
intended to settle, such as commercial invoices in
an accounts' receivable system."""
    
    def __init__(self,beneficiary:Participant,amount:float,end_to_end_id:str,remittance_information:str):
        """Initializes a transaction object
        """ 
        self.beneficiary = beneficiary
        self.amount = amount
        self.end_to_end_id = end_to_end_id
        self.remittance_information = remittance_information

class SCTInstC2B:
    """A class to represent a SCTInst C2B message
    """
    group_header:GroupHeader
    """`sepa_sctinst.sct_inst_c2b.GroupHeader` object shared by all individual transactions included in the message. """
    originator:Participant
    """Originator `sepa_sctinst.sct_inst_c2b.Participant` object that initiates the payment. """
    payment_information:PaymentInformation
    """`sepa_sctinst.sct_inst_c2b.PaymentInformation` object shared characteristics that applies to the debit side
of the payment transactions. """
    transactions:list
    """List of all `sepa_sctinst.sct_inst_c2b.Transaction`"""

    def __init__(self,group_header:GroupHeader,originator:Participant,payment_information:PaymentInformation,transactions:list):
        """Initializes a SCTInstC2B object
        """ 
        self.group_header = group_header
        self.originator = originator
        self.payment_information = payment_information
        self.transactions = transactions
        
    def add_transaction(self,transaction):
        self.transactions.append(transaction)

    @staticmethod
    def random(nb_txs):
        """Generate random SCTInstC2B object

        Returns:
            SCTInstC2B: SCTInstC2B object with random value
        """
        fake = Faker()
        
        group_header = GroupHeader('MSGID1234',datetime.today(),'Initiator Name')
        originator = Participant('BOUSFRPPXXX','FR7630001007941234567890185','The originator company')
        beneficiary = Participant('BOUSFRPPXXX','FR7630001007941234567890185','My beneficiary company')
        payment_inf = PaymentInformation("Payment-Information-ID",True,date.today())
        transation = Transaction(beneficiary,10.12,'end to end instr','remittance information')
        transation_2 = Transaction(beneficiary,30.12,'end to end instr','remittance information')
        sct_message = SCTInstC2B(group_header,originator,payment_inf,[])
        sct_message.add_transaction(transation)
        sct_message.add_transaction(transation_2)
        
        group_header = GroupHeader(fake.bothify(text='MSGID?????????'),fake.date_time(),'Initiator '+fake.name())
        originator = Participant(fake.lexify(text='????',letters='ABCDEFGRHIJKL') + fake.bank_country() + 'PPXXX',
                                 fake.iban(),fake.name())
        payment_inf = PaymentInformation('TXID?????????',fake.pybool(),fake.date_object())
        
        transactions = []
        
        for txs in range(nb_txs):
            
            beneficiary = Participant(fake.lexify(text='????',letters='ABCDEFGRHIJKL') + fake.bank_country() + 'PPXXX',
                                  fake.iban(),fake.name())
        
            transaction = Transaction(beneficiary,
                                    round(random.uniform(1,200), 2),
                                    fake.bothify(text='ENDTOEND?????????'),
                                    fake.bothify(text='REMINF?????????'))
            transactions.append(transaction)
    
        return SCTInstC2B(group_header,originator,payment_inf,transactions)
        
    

    def to_xml(self):
        """ Generate message as XML Document
        Returns a string as XML dcoument
        """
        
        if not self.transactions:
            raise ValueError("A minimum of one transaction is required")
        
        root = ET.Element("Document")
        root.set('xmlns',"urn:iso:std:iso:20022:tech:xsd:pain.001.001.03")
        root_fito = ET.SubElement(root, "CstmrCdtTrfInitn")
        
        self.xml_header(root_fito)
        self.xml_payment_information(root_fito)

        ET.ElementTree(root)
 
        return ET.tostring(root,encoding='utf-8',xml_declaration=True).decode('utf-8')

    def xml_transaction(self, root_fito,transaction):
        cdt_tx = ET.SubElement(root_fito, "CdtTrfTxInf")
        
        cdt_tx_pmt = ET.SubElement(cdt_tx, "PmtId")
        cdt_tx_pmt_e2e = ET.SubElement(cdt_tx_pmt, "EndToEndId")
        cdt_tx_pmt_e2e.text = transaction.end_to_end_id
        
        cdt_tx_pmt_amt = ET.SubElement(cdt_tx, "Amt")
        cdt_tx_pmt_inst_amt = ET.SubElement(cdt_tx_pmt_amt, "InstdAmt ")
        cdt_tx_pmt_inst_amt.set('Ccy',CURRENCY)
        cdt_tx_pmt_inst_amt.text = str(transaction.amount)
        
        Participant.to_xml(self,cdt_tx,transaction,'Cdtr')
            
        cdt_tx_pmt = ET.SubElement(cdt_tx, "RmtInf")
        cdt_tx_pmt_rem_inf = ET.SubElement(cdt_tx_pmt, "Ustrd")
        cdt_tx_pmt_rem_inf.text = transaction.remittance_information
        

    def xml_header(self, root_fito):
        
        sum_amount = self.sum_amounts()
        
        grp_header = ET.SubElement(root_fito, "GrpHdr")
        
        header_id = ET.SubElement(grp_header, "MsgId")
        header_id.text = str(self.group_header.message_identification)
        
        header_cre_dt_tm = ET.SubElement(grp_header, "CreDtTm")
        header_cre_dt_tm.text = str(self.group_header.creation_datetime.isoformat())
        
        header_nb_txs = ET.SubElement(grp_header, "NbOfTxs")
        header_nb_txs.text = str(len(self.transactions))
        
        header_ctrlsum = ET.SubElement(grp_header, "CtrlSum")
        header_ctrlsum.text = str(sum_amount)
        
        init_party = ET.SubElement(grp_header, "InitgPty")
        init_party_name = ET.SubElement(init_party, "Nm")
        init_party_name.text = self.group_header.init_party_name
        
        
    def xml_payment_information(self, root_fito):
        
        sum_amount = self.sum_amounts()
    
        payment_information = ET.SubElement(root_fito, "PmtInf")
        
        payment_information_id = ET.SubElement(payment_information, "PmtInfId")
        payment_information_id.text = self.payment_information.payment_id
        
        payment_information_method = ET.SubElement(payment_information, "PmtMtd")
        payment_information_method.text = PAYMENT_METHOD
        
        payment_information_method = ET.SubElement(payment_information, "BtchBookg")
        payment_information_method.text = str(self.payment_information.batch_booking).lower()
        
        payment_information_nb_txs = ET.SubElement(payment_information, "NbOfTxs")
        payment_information_nb_txs.text = str(len(self.transactions))

        payment_information_ctrlsum = ET.SubElement(payment_information, "CtrlSum")
        payment_information_ctrlsum.text = str(sum_amount)
        
        payment_information_req_exc_date = ET.SubElement(payment_information, "ReqdExctnDt")
        payment_information_req_exc_date.text = str(self.payment_information.requ_exe_date)
        
        Participant.to_xml(self,payment_information, None, 'Dbtr')
        
        payment_information_charge_bearer = ET.SubElement(payment_information, "ChrgBr")
        payment_information_charge_bearer.text = CHARGE_BEARER

        for transaction in self.transactions:
            self.xml_transaction(payment_information,transaction)

    def sum_amounts(self):
        sum_amount = 0
        if self.transactions:
            sum_amount = functools.reduce(lambda a, b: 
                a+b.amount if isinstance(a, float) else a.amount+b.amount
                , self.transactions)
        return sum_amount
            

