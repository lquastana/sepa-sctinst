from setuptools import setup

setup(name="sepa-sctinst",
      version="0.0.1",
      description="Tools for SCTInst payment scheme",
      author="lquastana",
      packages=["sepa_sctinst"],
      install_requires=["lxml","Faker"],
      extras_require={
            "dev": ["requests-mock"]
      },
      license="Apache 2.0")