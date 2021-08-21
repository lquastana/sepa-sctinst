from io import BytesIO, StringIO
import xml.etree.cElementTree as ET

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

    transactions=[]

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

    def add_transaction(self,transaction:Transaction):
        """ Add transaction

        Args:
            transaction (Transaction): Transaction
        """
        self.transactions.append(transaction)
    
    def to_xml(self):
        
        
        ET.register_namespace('',"urn:iso:std:iso:20022:tech:xsd:pacs.008.001.02")

        root = ET.Element("Document")
        doc = ET.SubElement(root, "FIToFICstmrCdtTrf")
        
        tree = ET.ElementTree(root)
        xml_buffer = BytesIO()
        tree.write(xml_buffer,
                   encoding='utf-8',
                   xml_declaration=True)
        
        
        return xml_buffer.read()


