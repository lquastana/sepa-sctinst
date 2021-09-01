from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name="sepa-sctinst",
      version="0.0.2",
      description="SEPA SCTInst is a python package that provides some features to manage SCTInst payments",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/lquastana/sepa-sctinst",
      author="lquastana",
      packages=["sepa_sctinst"],
      install_requires=["lxml","Faker"],
      extras_require={
            "dev": ["requests-mock"]
      },
      classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3',
            'Topic :: Software Development :: Libraries :: Python Modules'
        ],
      keywords='sepa sctinst',
      platforms='any',
      license="Apache 2.0")