from setuptools import setup

setup(name="sctinst",
      version="0.0.1",
      description="Tools for SCTInst payment scheme",
      author="laurent quastana",
      author_email="laurent.quastana@gmail.com",
      packages=["sctinst"],
      install_requires=["lxml"],
      extras_require={
            "dev": ["requests-mock"],
      },
      license="Apache 2.0")