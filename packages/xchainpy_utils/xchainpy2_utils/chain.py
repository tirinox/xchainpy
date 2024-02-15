from enum import Enum


class Chain(Enum):
    Binance = "BNB"
    Bitcoin = "BTC"
    Ethereum = "ETH"
    THORChain = "THOR"
    Cosmos = "GAIA"
    BitcoinCash = "BCH"
    Litecoin = "LTC"
    Doge = "DOGE"
    Avalanche = "AVAX"
    Maya = "MAYA"
    BinanceSmartChain = "BSC"
    Dash = "DASH"
    Kujira = "KUJI"

    UNKNOWN = 'Unknown'

    @property
    def is_utxo(self):
        return self in UTXO_CHAINS

    @property
    def is_evm(self):
        return self in EVM_CHAINS

    @property
    def is_cosmos(self):
        return self in COSMOS_CHAINS


UTXO_CHAINS = {Chain.Bitcoin, Chain.Litecoin, Chain.BitcoinCash, Chain.Doge, Chain.Dash}
EVM_CHAINS = {Chain.Ethereum, Chain.BinanceSmartChain, Chain.Avalanche}
COSMOS_CHAINS = {Chain.Cosmos, Chain.THORChain, Chain.Maya, Chain.Binance}
