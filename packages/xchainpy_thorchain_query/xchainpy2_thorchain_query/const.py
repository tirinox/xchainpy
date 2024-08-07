from xchainpy2_utils import NetworkType, Asset

DEFAULT_INTERFACE_ID = 'XChainPy2'
"""
    Default Interface ID. This is used to identify the client when making requests to the public data provider.
    If you don't attach an interface ID, the server may reject your request.
"""

TC_RESERVE_ADDR = 'thor1dheycdevq39qlkxs2a6wuuzyn4aqxhve4qxtxt'
"""Reserve module's address for THORChain."""

TC_BOND_ADDR = 'thor17gw75axcnr8747pkanye45pnrwk7p9c3cqncsv'
"""Bond module's address for THORChain."""

TC_POOL_ADDR = 'thor1g98cy3n9mmjrpn0sxmn63lztelera37n8n67c0'
"""Pool module's address for THORChain."""

TC_STANDBY_RESERVE_ADDR = 'thor1lj62pg6ryxv2htekqx04nv7wd3g98qf9gfvamy'
"""Standby reserve module's address for THORChain. Burnt."""


class Mimir:
    """
    This class holds some necessary Mimir constants names for THORChain.
    """

    HALT_TRADING = 'HALTTRADING'
    HALT_CHAIN_GLOBAL = 'HALTCHAINGLOBAL'
    PAUSE_LP = 'PAUSELP'
    MIN_TX_OUT_VOLUME_THRESHOLD = 'MINTXOUTVOLUMETHRESHOLD'
    MAX_TX_OUT_OFFSET = 'MAXTXOUTOFFSET'
    TX_OUT_DELAY_RATE = 'TXOUTDELAYRATE'
    FULL_IL_PROTECTION_BLOCKS = 'FULLIMPLOSSPROTECTIONBLOCKS'

    TNS_REGISTER_FEE = 'TNSREGISTERFEE'
    TNS_FEE_PER_BLOCK = 'TNSFEEPERBLOCK'

    RUNEPoolDepositMaturityBlocks = 'RUNEPoolDepositMaturityBlocks'

    @staticmethod
    def pause_lp(chain: str):
        """
        Returns the Mimir constant name for pausing liquidity provision on a chain.

        :param chain: Name of the chain
        :type chain: str
        :return: Mimir constant name
        :rtype: str
        """
        return f'PAUSELP{chain.upper()}'

    @staticmethod
    def halt_trading(chain):
        """
        Returns the Mimir constant name for halting trading on a chain.

        :param chain: Name of the chain
        :type chain: str
        :return: Mimir constant name
        :rtype: str
        """
        return f'HALT{chain.upper()}TRADING'


DEFAULT_EXTRA_ADD_MINUTES = 15
"""Default extra minutes to add to the current time for the deadline of a transaction."""

SAME_ASSET_EXCHANGE_RATE = 1.0

TEN_MINUTES = 60 * 10
"""Ten minutes in seconds."""

USD_ASSETS = {
    NetworkType.MAINNET: [
        Asset.from_string('BNB.BUSD-BD1'),
        Asset.from_string('ETH.USDC-0XA0B86991C6218B36C1D19D4A2E9EB0CE3606EB48'),
        Asset.from_string('ETH.USDT-0XDAC17F958D2EE523A2206206994597C13D831EC7'),
        Asset.from_string('ETH.DAI-0X6B175474E89094C44DA98B954EEDEAC495271D0F'),
        Asset.from_string('ETH.GUSD-0X056FD409E1D7A124BD7017459DFEA2F387B6D5CD'),
        Asset.from_string('ETH.LUSD-0X5F98805A4E8BE255A32880FDEC7F6728C6568BA0'),
        Asset.from_string('ETH.USDP-0X8E870D67F660D95D5BE530380D0EC0BD388289E1'),
        Asset.from_string('AVAX.USDC-0XB97EF9EF8734C71904D8002F8B6BC66DD9C48A6E'),
        Asset.from_string('BSC.USDC-0X8AC76A51CC950D9822D68B83FE1AD97B32CD580D'),
    ],
    NetworkType.STAGENET: [
        Asset.from_string('ETH.USDT-0XDAC17F958D2EE523A2206206994597C13D831EC7')
    ],
    NetworkType.TESTNET: [
        Asset.from_string('BNB.BUSD-74E'),
        Asset.from_string('ETH.USDT-0XA3910454BF2CB59B8B3A401589A3BACC5CA42306')
    ]
}
"""
    Stable USD assets for different networks types. The list is based on the pool list from THORChain.
    Subject to change.
"""

THORNAME_BLOCKS_ONE_YEAR = 5259600
"""Number of blocks in one year for THORChain."""


THOR_BLOCK_TIME_SEC = 6.0
"""Typical time in seconds for a block to be produced in THORChain."""
