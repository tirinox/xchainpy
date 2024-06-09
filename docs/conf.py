# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import datetime

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'XChainPy2'
author = 'Tirinox aka account1242'
copyright = f"{datetime.date.today().year}, {author}"

release = '0.0.2'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx_rtd_theme',
    'sphinx.ext.napoleon',
    'sphinx.ext.autosummary',
    'sphinx_copybutton',
    'sphinx.ext.autodoc'
]

# Configuration for autodoc
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
source_suffix = ".rst"


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']

html_logo = "_static/xchainpy2-logo.png"

import os
import sys

packages = [
    "xchainpy_utils",
    "xchainpy_client",
    "xchainpy_crypto",

    "xchainpy_bitcoin",
    "xchainpy_bitcoincash",
    "xchainpy_litecoin",
    "xchainpy_dogecoin",

    "xchainpy_ethereum",
    "xchainpy_avalanche",
    "xchainpy_arbitrum",
    "xchainpy_bsc",

    "xchainpy_cosmos",
    "xchainpy_thorchain",
    "xchainpy_mayachain",

    "xchainpy_thorchain_query",
    "xchainpy_thorchain_amm",

    # obsolete and other
    "xchainpy_binance",
    "xchainpy_utxo_providers",
]

for pack in packages:
    p = os.path.abspath(f'../packages/{pack}')
    if not os.path.exists(p):
        raise FileNotFoundError(f"Package {pack} not found at {p}")
    sys.path.insert(0, p)
