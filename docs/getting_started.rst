Quickstart
===============

What is it?
------------------------------------------------

**SEPA SCTInst** is a python package that provides some features to manage SCTInst payments.

Main Features
------------------------------------------------

Here are just a few of the things that sctinst does well:
- XSD validation
- SCTInst Scheme implementation
- Generate random payments

Where to get it
------------------------------------------------

The source code is currently hosted on GitHub at:
https://github.com/lquastana/sepa-sctinst.git

Binary installers for the latest released version are available at the [Python
Package Index (PyPI)](https://pypi.org/project/sepa-sctinst)

.. code-block:: shell

   pip install sepa-sctinst


Schema validation
------------------------------------------------

To validate a SCTInst XML message use the :class:`~sepa_sctinst.schema_validation.SchemaValidation` class.
To choose the type of message use the :class:`~sepa_sctinst.message.Message` class

 .. code-block:: python

    from sepa_sctinst.schema_validation import SchemaValidation
    from sepa_sctinst.default_messages import DefaultMessages

    with open('pacs008_valid.xml', 'r') as input:
        data = input.read()

    response = SchemaValidation.validate(data,DefaultMessages.SCTINST_INTERBANK)

    if response['isValid']:
        print('Valid message!')
    else:
        print(response['error_messages'])

If you don't know what type of message to use, call the :meth:`~sepa_sctinst.Message.autodetect` method.

 .. code-block:: python

    from sepa_sctinst.schema_validation import SchemaValidation
    from sepa_sctinst.message import Message

    with open('pacs008_valid.xml', 'r') as input:
        data = input.read()

    response = SchemaValidation.validate(data,Message.autodetect(data))


SCTInst Messages
------------------------------------------------

To generate an SCTInst message you can use the following class

:class:`sepa_sctinst.sct_inst_interbank.SCTInst` for Interbank messages

 .. code-block:: python

    from datetime import date,datetime
    from sepa_sctinst.sct_inst_interbank import SCTInst,GroupHeader,Transaction
    from sepa_sctinst.participant import Participant

    group_header = GroupHeader('MSGID1234',datetime.today(),date.today(),'CLRG')
    originator = Participant('BOUSFRPPXXX','FR7630001007941234567890185','The originator company')
    beneficiary = Participant('BOUSFRPPXXX','FR7630001007941234567890185','My beneficiary company')
    transation = Transaction(beneficiary,10.12,'end to end instr','tx id',datetime.now(),'reference','remittance information')
    sct_inst_interbank = SCTInst(group_header,originator,transation)

    xml_value = sct_inst_interbank.to_xml()

:class:`sepa_sctinst.sct_inst_c2b.SCTInstC2B` for C2B messages

 .. code-block:: python

    from datetime import date,datetime
    from sepa_sctinst.sct_inst_c2b import SCTInstC2B,GroupHeader,Transaction,PaymentInformation
    from sepa_sctinst.participant import Participant

    group_header = GroupHeader('MSGID1234',datetime.today(),'Initiator Name')
    originator = Participant('BOUSFRPPXXX','FR7630001007941234567890185','The originator company')
    beneficiary = Participant('BOUSFRPPXXX','FR7630001007941234567890185','My beneficiary company')
    payment_inf = PaymentInformation("Payment-Information-ID",True,date.today())
    transation = Transaction(beneficiary,10.12,'end to end instr','remittance information')
    transation_2 = Transaction(beneficiary,30.12,'end to end instr','remittance information')
    c2b_message = SCTInstC2B(group_header,originator,payment_inf,[])
    c2b_message.add_transaction(transation)
    c2b_message.add_transaction(transation_2)

    xml_value = c2b_message.to_xml()

The library offers a possibility to generate random messages

 .. code-block:: python

    from sepa_sctinst.sct_inst_interbank import SCTInst
    from sepa_sctinst.sct_inst_c2b import SCTInstC2B

    c2b_message = SCTInstC2B.random(nb_txs=4)
    interbank_message = SCTInst.random()

