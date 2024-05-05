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

release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx_rtd_theme',
    'sphinx.ext.autodoc'
]

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
]

for pack in packages:
    sys.path.insert(0, os.path.abspath(f'../packages/{pack}'))
