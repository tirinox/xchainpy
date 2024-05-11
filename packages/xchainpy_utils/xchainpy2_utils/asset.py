from typing import NamedTuple, Optional, Union

from .chain import Chain
from .util import XChainProtocol

SYNTH_DELIMITER = '/'
NON_SYNTH_DELIMITER = '.'


def get_delimiter(synth: bool):
    """
    Get the delimiter based on whether the asset is a synth or not.
    Native assets use '.' as delimiter (THOR.RUNE) while synth assets use '/' as delimiter (BTC/BTC).
    """
    return SYNTH_DELIMITER if synth else NON_SYNTH_DELIMITER


class Asset(NamedTuple):
    """
    Asset is used to identify a blockchain asset in the cross-chain environment.
    It has chain, symbol, and contract fields.

    .. py:attribute:: chain

            The blockchain identifier. E.g. 'BNB', 'ETH', 'BTC', etc.
            This field has type str. Be careful to not confuse this with the Chain object.

    .. py:attribute:: symbol

            The asset symbol. E.g. 'RUNE', 'BTC', 'ETH', etc.

    .. py:attribute:: contract

            The contract address of the asset. E.g. '0x1234...5678'. Default is empty.

    """
    chain: str
    symbol: str
    contract: str = ''
    synth: bool = False

    @property
    def is_valid(self):
        """
        Check if the asset is valid. An asset is valid if it has both chain and symbol.
        """
        return self.chain and self.symbol

    @property
    def delimiter(self):
        """
        Get the delimiter based on whether the asset is a synth or not.
        Synth assets use '/' as delimiter (BTC/BTC) while non-synth (native) assets use '.' as delimiter (THOR.RUNE).
        """
        return SYNTH_DELIMITER if self.synth else NON_SYNTH_DELIMITER

    def __str__(self):
        """
        Convert the asset to a full string representation. Like CHAIN.SYMBOL-CONTRACT
        """
        s = f'{self.chain}{self.delimiter}{self.symbol}'
        if self.contract:
            s += f'-{self.contract}'
        return s

    def __repr__(self):
        return f"Asset({self!s})"

    @staticmethod
    def get_name_and_contract(input_str):
        """
        Get the name and contract from the input string.
        :param input_str: The input string to parse
        :return: A tuple containing the name and contract
        """
        components = input_str.split('-', maxsplit=2)
        if len(components) == 2:
            return components
        else:
            return input_str, ''

    @classmethod
    def from_string(cls, s) -> Optional['Asset']:
        """
        Create an Asset object by parsing the input string.
        If the input string is already an Asset object, it will be returned as is.
        The format of the input string should be CHAIN.SYMBOL-CONTRACT. Synth assets should use '/' as delimiter.
        If you pass a string with only the symbol (e.g. ETH), it will be used as both symbol and ticker: ETH.ETH
        This method does not recognize short codes like 'rune' or 'btc' and does not do any case conversion.
        See Asset.automatic() for that.
        :param s: The input string to parse
        :return: An Asset object if the input string is valid, otherwise None
        """
        if isinstance(s, Asset):
            return s

        if not isinstance(s, str):
            raise ValueError(f'Asset string must be a string, not {type(s)}')

        s = s.strip()

        is_synth = SYNTH_DELIMITER in s
        data = s.split(get_delimiter(is_synth))
        n = len(data)
        if n == 1:
            if symbol := data[0]:
                return cls(symbol, symbol)
        elif n == 2:
            name, tag = cls.get_name_and_contract(data[1])
            return cls(data[0], name, tag, is_synth)

    @classmethod
    def from_string_exc(cls, s) -> Optional['Asset']:
        """
        Create an Asset object by parsing the input string.
        The difference between this method and from_string is that this method raises a ValueError
        if the input string is invalid.
        """
        a = cls.from_string(s)
        if a is None:
            raise ValueError(f'Invalid asset string: {s}')
        return a

    @classmethod
    def automatic(cls, x) -> Optional['Asset']:
        """
        Create an Asset object by parsing the input string.
        This method recognizes short codes like 'rune' or 'btc' and converts the input string to uppercase.
        :param x: The input string to parse
        :return: An Asset object if the input string is valid, otherwise None
        """
        if isinstance(x, str):
            if (x_low := x.lower()) in CommonAssets.SHORT_CODES:
                return CommonAssets.SHORT_CODES[x_low]
            return cls.from_string(x).upper()
        elif isinstance(x, Asset):
            return x.upper()

    @property
    def as_native(self):
        """
        Get a native copy of the asset object. Native assets use '.' as delimiter (THOR.RUNE).
        :return: A native version of the asset.
        """
        # noinspection PyArgumentEqualDefault
        return self._replace(synth=False)

    @property
    def as_synth(self):
        """
        Get a synth copy of the asset object. Synth assets use '/' as delimiter (BTC/BTC).
        :return: A synth version of the asset.
        """
        return self._replace(synth=True)

    @property
    def is_rune_native(self):
        return self.chain == 'THOR' and self.symbol == 'RUNE'

    def is_native(self, p: XChainProtocol = XChainProtocol.THORCHAIN):
        if p == XChainProtocol.THORCHAIN:
            return self == AssetRUNE
        elif p == XChainProtocol.MAYA:
            return self == AssetCACAO

    @property
    def ticker(self):
        """
        Get the ticker of the asset. Same as symbol.
        """
        return self.symbol

    @property
    def full_symbol(self):
        """
        Get the full symbol of the asset including its contract if it has one.
        E.g. USDT-0XDAC17F958D2EE523A2206206994597C13D831EC7.
        """
        return f"{self.symbol}-{self.contract}" if self.contract else self.symbol

    @classmethod
    def dummy(cls):
        """
        Get a dummy asset with empty chain, symbol, and contract.
        """
        return cls('', '')

    @property
    def is_gas(self):
        """
        Check if the asset is a gas asset for its chain.
        """
        return is_gas_asset(self)

    def upper(self):
        """
        Get an upper case version of the asset. All fields will be converted to upper case.
        """
        return self._replace(
            symbol=self.symbol.upper(),
            contract=self.contract.upper(),
            chain=self.chain.upper() if self.chain else self.chain
        )

    def __eq__(self, other: 'Asset'):
        """
        Check if two assets are equal. Both asset will be converted to upper case before comparison.
        """
        if not isinstance(other, Asset):
            return False
        a, b = self.upper(), other.upper()
        return a.chain == b.chain and a.symbol == b.symbol and a.contract == b.contract and a.synth == b.synth


AssetBTC = Asset.from_string('BTC.BTC')
AssetETH = Asset.from_string('ETH.ETH')
AssetBNB = Asset.from_string('BNB.BNB')
AssetBSC = Asset.from_string('BSC.BNB')
AssetBCH = Asset.from_string('BCH.BCH')
AssetLTC = Asset.from_string('LTC.LTC')
AssetDOGE = Asset.from_string('DOGE.DOGE')
AssetAVAX = Asset.from_string('AVAX.AVAX')
AssetAEth = Asset.from_string('ARB.ETH')
AssetRUNE = Asset.from_string('THOR.RUNE')
AssetATOM = Asset.from_string('GAIA.ATOM')
AssetCACAO = Asset.from_string('MAYA.CACAO')
AssetDASH = Asset.from_string('DASH.DASH')


def get_chain_gas_asset(chain: Union[Chain, str]) -> Asset:
    """
    Get the gas asset for the specified chain.
    :param chain: The chain to get the gas asset for. Can be a Chain object or a string.
    :raise ValueError: If the chain is not recognized.
    :return: The gas Asset for the specified chain.
    """
    if isinstance(chain, str):
        chain = Chain(chain)

    if chain == Chain.Bitcoin:
        return AssetBTC
    elif chain == Chain.BitcoinCash:
        return AssetBCH
    elif chain == Chain.Litecoin:
        return AssetLTC
    elif chain == Chain.Doge:
        return AssetDOGE
    elif chain == Chain.Binance:
        return AssetBNB
    elif chain == Chain.Ethereum:
        return AssetETH
    elif chain == Chain.Avalanche:
        return AssetAVAX
    elif chain == Chain.Cosmos:
        return AssetATOM
    elif chain == Chain.BinanceSmartChain:
        return AssetBSC
    elif chain == Chain.THORChain:
        return AssetRUNE
    elif chain == Chain.Maya:
        return AssetCACAO
    else:
        raise ValueError(f"Could not get gas asset for {chain} chain")


def is_gas_asset(asset: Asset) -> bool:
    """
    Check if the asset is a gas asset for its chain.
    :param asset: The asset to check
    :return: True if the asset is a gas asset, otherwise False
    """
    # todo: should we check for synth?
    return get_chain_gas_asset(Chain(asset.chain)) == asset


class CommonAssets:
    """
    Common assets used in the cross-chain environment and their short codes.
    """
    BTC = AssetBTC
    ETH = AssetETH
    BNB = AssetBNB
    BSC = AssetBSC
    BCH = AssetBCH
    LTC = AssetLTC
    DOGE = AssetDOGE
    AVAX = AssetAVAX
    AEth = AssetAEth
    RUNE = AssetRUNE
    ATOM = AssetATOM
    CACAO = AssetCACAO
    DASH = AssetDASH

    SHORT_CODES = {
        'a': AssetAVAX,
        'b': AssetBTC,
        'c': AssetBCH,
        'd': AssetDOGE,
        'e': AssetETH,
        'g': AssetATOM,
        'l': AssetLTC,
        'n': AssetBNB,
        's': AssetBSC,
        'r': AssetRUNE,
    }

    INVERTED_SHORT_CODES = {v: k for k, v in SHORT_CODES.items()}


def get_short_code(asset: Asset) -> str:
    """
    Get the short code for the specified asset.
    :param asset: The asset to get the short code for
    :return: The short code for the asset
    """
    return CommonAssets.INVERTED_SHORT_CODES.get(asset, '')
