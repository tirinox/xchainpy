from setuptools import setup, find_packages  # noqa: H301

NAME = "xchainpy_util"
VERSION = "0.0.1"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = []

setup(
    name=NAME,
    version=VERSION,
    description="XChainpy Utils",
    author_email="developer@tirinox.ru",
    url="",
    keywords=["Crypto", "XChain"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""XChainpy Utils"""
)
