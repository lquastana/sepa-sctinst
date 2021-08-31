import xml.etree.ElementTree as ET



class Participant:
    """A class to represent a participant in interbank SCTInst message
    """
    
    bic:str
    """The BIC code of the participant Bank"""
    iban:str
    """The IBAN of the account"""
    name:str
    """The name of the account"""
    
      
    def __init__(self,bic:str,iban:str,name:str):
        """Initializes a participant object
        """  
        self.bic = bic
        self.iban = iban
        self.name = name
    
    @staticmethod  
    def to_xml(payment, transaction_node:ET.SubElement,transaction, stakeholder:str):
        stakeholder_node = ET.Element(stakeholder)
        stakeholder_name = ET.SubElement(stakeholder_node, 'Nm')
        if stakeholder == 'Dbtr':
            stakeholder_name.text = payment.originator.name
        else:
            stakeholder_name.text = transaction.beneficiary.name
        
        stakeholder_acct = ET.Element(stakeholder+'Acct')
        stakeholder_acct_id = ET.SubElement(stakeholder_acct, 'Id')
        stakeholder_acct_iban = ET.SubElement(stakeholder_acct_id, 'IBAN')
        if stakeholder == 'Dbtr':
            stakeholder_acct_iban.text = payment.originator.iban
        else:
            stakeholder_acct_iban.text = transaction.beneficiary.iban
        
        stakeholder_agt = ET.Element(stakeholder+'Agt')
        stakeholder_agt_fin_inst = ET.SubElement(stakeholder_agt, 'FinInstnId')
        stakeholder_agt_fin_inst_bic = ET.SubElement(stakeholder_agt_fin_inst, 'BIC')
        if stakeholder == 'Dbtr':
            stakeholder_agt_fin_inst_bic.text = payment.originator.bic
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