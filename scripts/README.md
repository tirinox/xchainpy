## OpenAPI specification urls:
THORNode:
https://thornode.ninerealms.com/thorchain/doc/openapi.yaml

MayaNode:
https://mayanode.mayachain.info/mayachain/doc/openapi.yaml

Midgard (TC):
https://midgard.mayachain.info/v2/swagger.json


### Fix setup.py

In order to have a nice description in pypi you need to add the following to your setup.py

```python
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
    description="Thornode API",
    author_email="devs@thorchain.org",
    url="",
    keywords=["Swagger", "Thornode API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description=load_description(),   # (!) here
    long_description_content_type="text/markdown",
)
```

### Manual fix of None in transaction details

Go to `xchainpy2_thornode/models/tx_details_response.py`
Comment out lines 171-172 amd 194-195

```python
    @actions.setter
    def actions(self, actions):
        """Sets the actions of this TxDetailsResponse.


        :param actions: The actions of this TxDetailsResponse.  # noqa: E501
        :type: list[TxOutItem]
        """
        # if actions is None:
        #     raise ValueError("Invalid value for `actions`, must not be `None`")  # noqa: E501

        self._actions = actions
        
    @out_txs.setter
    def out_txs(self, out_txs):
        """Sets the out_txs of this TxDetailsResponse.


        :param out_txs: The out_txs of this TxDetailsResponse.  # noqa: E501
        :type: list[Tx]
        """
        # if out_txs is None:
        #     raise ValueError("Invalid value for `out_txs`, must not be `None`")  # noqa: E501

        self._out_txs = out_txs
```
