<div align="left">
  <img style="width: 40%" src="./SCTInst.jpg">
</div>

# SCTInst: powerful Python Sepa toolkit
[![codecov](https://codecov.io/gh/lquastana/sctinst/branch/main/graph/badge.svg?token=15NMHC642N)](https://codecov.io/gh/lquastana/sctinst)

## What is it?

**SCTInst** is a python package that provides some features to manage SCTInst payment.

## Main Features

Here are just a few of the things that sctinst does well:
- XSD validation
- PACS008 Scheme implementation

## Where to get it

The source code is currently hosted on GitHub at:
https://github.com/lquastana/sctinst.git

Binary installers for the latest released version are available at the [Python
Package Index (PyPI)](https://pypi.org/project/sctinst)

```sh
pip install pandas
```

## Dependencies

- [lxml](https://lxml.de/) - lxml is the most feature-rich and easy-to-use library for processing XML and HTML in the Python language.

## Installation from sources

In the `root` directory (same one where you found this file after
cloning the git repo), execute:

```sh
python -m pip install -e .
```

## Documentation

The official documentation is hosted on xxx.org: https://xxx.pydata.org/xxx-docs/stable


<!-- 
pytest --cov=sctinst
pdoc --html --output-dir ./doc ./sctinst/

-->
