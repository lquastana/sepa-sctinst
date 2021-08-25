<div align="left">
  <img style="width: 40%" src="./SCTInst.jpg">
</div>

# SEPA SCTInst: A powerful Python SEPA toolkit for SCTInst Payments
[![PyPI version](https://badge.fury.io/py/sepa-sctinst.svg)](https://badge.fury.io/py/sepa-sctinst)
[![codecov](https://codecov.io/gh/lquastana/sepa-sctinst/branch/main/graph/badge.svg?token=15NMHC642N)](https://codecov.io/gh/lquastana/sepa-sctinst)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=lquastana_sepa-sctinst&metric=alert_status)](https://sonarcloud.io/dashboard?id=lquastana_sepa-sctinst)
[![Documentation Status](https://readthedocs.org/projects/sepa-sctinst/badge/?version=latest)](https://sepa-sctinst.readthedocs.io/en/latest/?badge=latest)

## What is it?

**SEPA SCTInst** is a python package that provides some features to manage SCTInst payments.

## Main Features

Here are just a few of the things that sctinst does well:
- XSD validation
- SCTInst Scheme implementation
- Generate random payments

## Where to get it

The source code is currently hosted on GitHub at:
https://github.com/lquastana/sepa-sctinst.git

Binary installers for the latest released version are available at the [Python
Package Index (PyPI)](https://pypi.org/project/sepa-sctinst)

```sh
pip install sepa-sctinst
```

## Dependencies

- [lxml](https://lxml.de/) - lxml is the most feature-rich and easy-to-use library for processing XML and HTML in the Python language.
- [Faker](https://faker.readthedocs.io/en/master/) - Faker is a Python package that generates fake data for you.

## Installation from sources

In the `root` directory (same one where you found this file after
cloning the git repo), execute:

```sh
python -m pip install -e .
```

## Documentation

The official documentation generated with [sphinx](https://www.sphinx-doc.org/en/master/index.html) and hosted on Github: https://sepa-sctinst.readthedocs.io/


<!-- 
pytest --cov=sepa_sctinst
pdoc --output-dir ./docs ./sepa_sctinst
python -m build
python -m twine upload --repository pypi dist/*
-->
