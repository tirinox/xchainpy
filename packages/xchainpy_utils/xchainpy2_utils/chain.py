from enum import Enum


class Chain(Enum):
    """
    Enum representing the different chains supported by this library.
    These values must correspond to the chain names in THORChain; do not change them without a good reason.
    """

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
    Arbitrum = "ARB"
    Base = "BASE"
    Ripple = "XRP"
    Solana = "SOL"

    UNKNOWN = 'Unknown'

    @property
    def is_utxo(self):
        """
        Returns True if the chain is a UTXO chain (Bitcoin, Litecoin, BitcoinCash, Doge, Dash)
        :return: True if the chain is a UTXO chain
        """
        return self in UTXO_CHAINS

    @property
    def is_evm(self):
        """
        Returns True if the chain is an EVM chain (Ethereum, BinanceSmartChain, Avalanche, Arbitrum)
        :return: True if the chain is an EVM chain
        """
        return self in EVM_CHAINS

    @property
    def is_cosmos(self):
        """
        Returns True if the chain is a Cosmos-based chain (Cosmos, THORChain, Maya, Binance)
        :return: True if the chain is a Cosmos-based chain
        """
        return self in COSMOS_CHAINS

    @property
    def currency_symbol(self):
        """
        Returns the currency symbol for the chain.
        :return: The currency symbol for the chain.
        """
        return CURRENCY_SYMBOLS.get(self, '')


UTXO_CHAINS = {Chain.Bitcoin, Chain.Litecoin, Chain.BitcoinCash, Chain.Doge, Chain.Dash}
"""
UTXO_CHAINS is a set of chains that use the UTXO model.
"""

EVM_CHAINS = {Chain.Ethereum, Chain.BinanceSmartChain, Chain.Avalanche, Chain.Arbitrum, Chain.Base}
"""
EVM_CHAINS is a set of chains that are based on the Ethereum Virtual Machine (EVM).
"""

COSMOS_CHAINS = {Chain.Cosmos, Chain.THORChain, Chain.Maya}
"""
COSMOS_CHAINS is a set of chains that are based on the Cosmos SDK.
"""

CURRENCY_SYMBOLS = {
    Chain.Bitcoin: "₿",
    Chain.Litecoin: "Ł",
    Chain.BitcoinCash: "₿",
    Chain.Doge: "Ð",
    Chain.Ethereum: "Ξ",
    Chain.Maya: "𐌂",
    Chain.THORChain: "ᚱ",
}
"""
CURRENCY_SYMBOLS is a dictionary that maps each chain to its currency symbol.
"""
