# coding: utf-8

"""
    Mayanode API

    Mayanode REST API.  # noqa: E501

    OpenAPI spec version: 1.109.0
    Contact: devs@mayachain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from setuptools import setup, find_packages  # noqa: H301

NAME = "xchainpy2-mayanode"
VERSION = "1.109.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil"]
REQUIRES.append("aiohttp")


def load_description():
    """
    In setup call you do:
    long_description=load_description(),
    long_description_content_type="text/markdown",
    :return: text
    """
    from pathlib import Path
    this_directory = Path(__file__).parent
    long_description = (this_directory / "README.md").read_text()
    return long_description


setup(
    name=NAME,
    version=VERSION,
    description="Mayanode API",
    author_email="devs@mayachain.org",
    url="",
    keywords=["Swagger", "Mayanode API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description=load_description(),
    long_description_content_type="text/markdown",
)
