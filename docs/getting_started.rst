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
To choose the type of message use the :class:`~sepa_sctinst.Message` class
 .. code-block:: python

    from sepa_sctinst.schema_validation import SchemaValidation
    from sepa_sctinst import Message

    with open(filename, 'r') as input:
        data = input.read()
    
    response = schema_validation.validate(data,Message.SCTINST)

    if response['isValid']:
        print('Valid message!')
    else:
        print(response['error_messages'])

If you don't know what type of message to use, call the :meth:`~sepa_sctinst.MessageConfiguration.autodetect` method.

 .. code-block:: python

    from sepa_sctinst.schema_validation import SchemaValidation
    from sepa_sctinst import Message,MessageConfiguration

    with open(filename, 'r') as input:
        data = input.read()
    
    response = schema_validation.validate(
        data,
        MessageConfiguration.autodetect(data))





