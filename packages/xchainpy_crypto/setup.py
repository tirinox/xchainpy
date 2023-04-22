from pathlib import Path

from setuptools import setup, find_packages  # noqa: H301

NAME = "xchainpy2_crypto"
VERSION = "0.0.2"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "bip-utils>=2.7.0,<3.0.0",
    "pycrypto>=2.6.1,<3.0.0",
]


CWD = Path(__file__).resolve().parent

setup(
    name=NAME,
    version=VERSION,
    description="XChainPy2 Crypto",
    author_email="developer@tirinox.ru",
    url="https://github.com/tirinox/xchainpy/tree/develop/packages/xchainpy_crypto",
    keywords=["Crypto", "XChain"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="\n".join(
        (
            (CWD / "README.md").read_text(),
            # (CWD / "CHANGELOG.rst").read_text(),
        )
    )
)
