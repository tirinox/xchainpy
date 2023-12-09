from decimal import Decimal

from xchainpy2_utils import Amount, CryptoAmount, AssetRUNE, AssetCACAO, CACAO_DECIMAL, RUNE_DECIMAL

DEFAULT_INTERFACE_ID = 'XChainPy2'

TC_RESERVE_ADDR = 'thor1dheycdevq39qlkxs2a6wuuzyn4aqxhve4qxtxt'
TC_BOND_ADDR = 'thor17gw75axcnr8747pkanye45pnrwk7p9c3cqncsv'
TC_POOL_ADDR = 'thor1g98cy3n9mmjrpn0sxmn63lztelera37n8n67c0'
TC_STANDBY_RESERVE_ADDR = 'thor1lj62pg6ryxv2htekqx04nv7wd3g98qf9gfvamy'


class Mimir:
    HALT_TRADING = 'HALTTRADING'
    HALT_CHAIN_GLOBAL = 'HALTCHAINGLOBAL'
    PAUSE_LP = 'PAUSELP'
    MIN_TX_OUT_VOLUME_THRESHOLD = 'MINTXOUTVOLUMETHRESHOLD'
    MAX_TX_OUT_OFFSET = 'MAXTXOUTOFFSET'
    TX_OUT_DELAY_RATE = 'TXOUTDELAYRATE'
    FULL_IL_PROTECTION_BLOCKS = 'FULLIMPLOSSPROTECTIONBLOCKS'

    @staticmethod
    def pause_lp(chain):
        return f'PAUSELP{chain.upper()}'

    @staticmethod
    def halt_trading(chain):
        return f'HALT{chain.upper()}TRADING'


ETH_DECIMALS = 18
AVAX_DECIMALS = 18

DEFAULT_RUNE_NETWORK_FEE = CryptoAmount(Amount.from_asset(Decimal("0.02"), RUNE_DECIMAL), AssetRUNE)
DEFAULT_CACAO_NETWORK_FEE = CryptoAmount(Amount.from_asset(Decimal("0.5"), CACAO_DECIMAL), AssetCACAO)

DEFAULT_EXTRA_ADD_MINUTES = 15
