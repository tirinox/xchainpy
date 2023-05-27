from pathlib import Path

from setuptools import setup, find_packages  # noqa: H301

NAME = "xchainpy2_thorchain_query"
VERSION = "0.0.3"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    'aiohttp>=3.8.0,<4.0.0',
    'aiohttp-retry>=2.3.0,<3.0.0',

    # todo: make sure that all of these are correct
    'xchainpy2_util',
    'xchainpy2_crypto',
    'xchainpy2_midgard',
    'xchainpy2_thornode',
    'xchainpy2_mayanode',
]

CWD = Path(__file__).resolve().parent

setup(
    name=NAME,
    version=VERSION,
    description=(
        "XChainpy THORChain Query: "
        "Thorchain-query module to query thorchain for estimation of swaps/add "
        "and remove Liquidity and checking a transaction stage. "
        "Returns a TxDetail object with all the information needed to conduct a swap, or add liquidity. "
        "This includes estimateAddSavers()"
    ),
    author_email="developer@tirinox.ru",
    url="https://github.com/tirinox/xchainpy/tree/develop/packages/xchainpy_thorchain_query",
    keywords=["Crypto", "XChain", "THORChain"],
    install_requires=REQUIRES,
    packages=find_packages('xchainpy2_thorchain_query'),
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
