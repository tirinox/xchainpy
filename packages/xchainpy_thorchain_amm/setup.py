from pathlib import Path

from setuptools import setup, find_packages  # noqa: H301

NAME = "xchainpy2_thorchain_amm"
VERSION = "0.0.4"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "bip-utils>=2.7.0,<3.0.0",
    "pycryptodome>=3.17,<4.0",
    "xchainpy2_utils>=0.0.4",
    "xchainpy2_crypto>=0.0.4",
    "xchainpy2_client>=0.0.4",
    "xchainpy2_thorchain>=0.0.4",
    "xchainpy2_cosmos>=0.0.4",
    "xchainpy2_query>=0.0.4",

]

CWD = Path(__file__).resolve().parent

setup(
    name=NAME,
    version=VERSION,
    description="XChainPy2 THORChain Automated Market Maker (AMM)",
    author_email="developer@tirinox.ru",
    url="https://github.com/tirinox/xchainpy/tree/develop/packages/xchainpy_crypto",
    keywords=["Crypto", "XChain", "THORChain", "Blockchain", "AMM", "Crosschain", "Wallet"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="\n".join(
        (
            (CWD / "README.md").read_text(),
            # (CWD / "CHANGELOG.rst").read_text(),
        )
    ),
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
