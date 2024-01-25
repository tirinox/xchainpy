import asyncio
from getpass import getpass

from xchainpy2_crypto import KeyStore
from xchainpy2_mayachain import MayaChainClient, DEFAULT_CLIENT_URLS
from xchainpy2_mayanode import ApiClient as MayaApiClient, NetworkApi as MayaNetworkApi
from xchainpy2_thorchain import THORChainClient
from xchainpy2_thorchain_amm import THORMemo
from xchainpy2_thorchain_query import URLs
from xchainpy2_thornode import ApiClient as ThorApiClient
from xchainpy2_utils import NetworkType

KS_PATH = "path_to_keystore.txt"
CACAO_ADD_AMOUNT = 10.0  # 10 cacao
RUNE_ADD_AMOUNT = 2.0  # 2 rune


async def load_clients():
    key_store = KeyStore.from_file(KS_PATH)

    password = getpass("Enter keystore password:")
    phrase = key_store.decrypt_from_keystore(password)

    maya = MayaChainClient(phrase=phrase)
    thor = THORChainClient(phrase=phrase)

    return maya, thor


async def main():
    thor_node_api = ThorApiClient()
    thor_node_api.configuration.host = URLs.THORNode.NINE_REALMS

    maya_node_api = MayaApiClient()
    maya_node_api.configuration.host = DEFAULT_CLIENT_URLS[NetworkType.MAINNET].node

    maya_network_api = MayaNetworkApi(maya_node_api)

    maya_inbound = await maya_network_api.inbound_addresses()
    thor_inbound = next(inb for inb in maya_inbound if inb.chain == 'THOR')
    print(f"THORChain inbound: {thor_inbound.address}")

    maya, thor = await load_clients()

    print('-----------------------------------------------------------------------------------------------------------')
    maya_address = maya.get_address()
    maya_balances = await maya.get_balance()
    print(f"Maya address: {maya_address} balances: {maya_balances}")

    thor_address = thor.get_address()
    thor_balances = await thor.get_balance()
    print(f"Thor address: {thor_address} balances: {thor_balances}")

    thor_side_memo = THORMemo.add_liquidity('THOR.RUNE', maya_address).build()
    maya_side_memo = THORMemo.add_liquidity('THOR.RUNE', thor_address).build()

    print('-----------------------------------------------------------------------------------------------------------')
    print(f"THOR add memo: {thor_side_memo}")
    print(f"Maya add memo: {maya_side_memo}")

    print('-----------------------------------------------------------------------------------------------------------')
    print('Depositing CACAO to MayaChain...')
    txid = await maya.deposit(maya.gas_amount(float(CACAO_ADD_AMOUNT)), memo=maya_side_memo)
    print(f"Maya deposit txid: {maya.get_explorer_tx_url(txid)}")

    input('Press enter when deposit is confirmed.')

    print('-----------------------------------------------------------------------------------------------------------')
    print('Sending Rune to the inbound address of MayaChain...')
    txid = await thor.transfer(thor.gas_amount(float(RUNE_ADD_AMOUNT)), thor_inbound.address, memo=thor_side_memo)
    print(f"Thor transfer txid: {thor.get_explorer_tx_url(txid)}")

    print('-----------------------------------------------------------------------------------------------------------')
    print('Done!')

    await maya_node_api.rest_client.pool_manager.close()
    await thor_node_api.rest_client.pool_manager.close()


if __name__ == '__main__':
    asyncio.run(main())
