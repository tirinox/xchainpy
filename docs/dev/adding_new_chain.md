Adding a new chain client
--------------------------

If you want to add a new chain to the XChainPy2 library, follow the steps below:

1. Create a new folder in the `packages/xchainpy_CHAIN` directory with the name of the chain you want to add.
2. Add LICENSE, README.md. A good point to start is to copy the files from any other client folder.
3. Copy and edit `pyproject.toml`
    - Change the `name` field to `xchainpy_CHAIN`
    - Change the `description` field to something like `XChainPy2 client for the CHAIN chain`
    - Fill `keywords`
    - Fill `dependencies` with the required dependencies for the chain client
4. Create a new folder `packages/xchainpy_CHAIN/xchainpy2_CHAIN`
5. Write the chain client code in the new folder (yeah, that's the hard part)
6. Add `__init__.py` file that imports all the necessary classes and functions
7. Write some tests in the `tests` folder
8. Go to `docs/index.md` and add mention of the new chain client (you will easily find where to add it)
9. Go to `docs/conf.py` and add the newly added package to the list of `packages`
10. Go to `docs/requirements.txt` and add the package to the list of `packages/xchainpy_CHAIN`
11. At the end, run `make publish` to publish the package.
12. Go to `packages/xchainpy_wallet/xchainpy2_wallet/detect_clients.py` and add a piece of code like this

```python
try:
    from xchainpy2_Chain import YourChainClient
except ImportError:
    YourChainClient = NoClient
```

12. Also, there you a reference to the client class to `CLIENT_CLASSES` dict.
