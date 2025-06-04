from contextlib import suppress
from enum import Enum
from typing import NamedTuple, Optional, Union

from .chain import Chain

SYNTH_DELIMITER = '/'
"""Synth assets use '/' as delimiter (BTC/BTC)"""

TRADE_DELIMITER = '~'
"""Trade assets use '~' as delimiter (BTC~BTC)"""

NATIVE_DELIMITER = '.'
"""Native assets use '.' as delimiter (THOR.RUNE, BTC.BTC)"""

SECURED_DELIMITER = '-'
"""
    Secured assets use '-' as delimiter (ETH-ETH).
    See: https://docs.thorchain.org/thorchain-finance/secured-assets
"""

ALL_DELIMITERS = {SYNTH_DELIMITER, TRADE_DELIMITER, NATIVE_DELIMITER, SECURED_DELIMITER}


class AssetKind(Enum):
    NATIVE = 'native'
    """Native Assets are L1 assets (eg BTC) available on its native L1 (eg Bitcoin Network)."""

    SYNTH = 'synth'
    """
    THORChain synthetics are fully collateralized while they exist and switch to a 1:1 peg upon redemption.
    See: https://docs.thorchain.org/frequently-asked-questions/asset-types#synthetic-assets
    Attention! Synthetic assets are now suspended on the network due to THORFi being on pause.
    Please use trade and secured assets instead.
    """
    # todo: fill in the details for derived assets

    TRADE = 'trade'
    """
    Trade Assets, a new class of primitives on THORChain, offer double the capital efficiency of synthetic assets, 
    enhancing arbitrage and high-frequency trading. They settle with THORChain’s block speed and cost, enabling 
    6-second finality swaps without high fees. Redeemable anytime with no slippage, Trade Assets emulate centralized 
    exchange trading but maintain on-chain transparency and security. Custodied by THORChain outside of liquidity pools, 
    they provide user credits while holding funds 1:1 as L1 assets until withdrawal, making THORChain more user-friendly 
    for active traders.
    See: https://docs.thorchain.org/frequently-asked-questions/asset-types#trade-assets
    """

    DERIVED = 'derived'
    """
    THORChain derived assets.
    See: https://docs.thorchain.org/frequently-asked-questions/asset-types#derived-assets
    """

    SECURED = 'secured'
    """
    Secure Assets allow L1 tokens to be deposited to THORChain, creating a new native asset, which can be transferred 
    between accounts, over IBC and integrated with CosmWasm smart contracts using standard Cosmos SDK messages. 
    They also replace Trade Assets. 
    See: https://docs.thorchain.org/thorchain-finance/secured-assets
    """

    UNKNOWN = 'unknown'
    """Unknown asset type."""

    @property
    def delimiter(self):
        """
        Return the delimiter based on the asset kind.
        """
        if self == AssetKind.SYNTH:
            return SYNTH_DELIMITER
        elif self == AssetKind.TRADE:
            return TRADE_DELIMITER
        elif self == AssetKind.SECURED:
            return SECURED_DELIMITER
        else:
            return NATIVE_DELIMITER

    @classmethod
    def recognize(cls, asset_str: str) -> 'AssetKind':
        """
            Detects the asset type based on the first delimiter in the asset string.

            :param asset_str: The asset string (e.g., "ETH.ETH", "BTC-BTC", "XRP~XRP").
            :return: The asset type: "trade" for "~", "secured" for "-", "native" for ".", or "unknown" if no valid delimiter is found.
            :rtype AssetKind
        """
        for char in asset_str:
            if char in ALL_DELIMITERS:
                return _DELIMITER_TABLE[char]
        return cls.UNKNOWN


_DELIMITER_TABLE = {
    TRADE_DELIMITER: AssetKind.TRADE,
    SECURED_DELIMITER: AssetKind.SECURED,
    NATIVE_DELIMITER: AssetKind.NATIVE,
    SYNTH_DELIMITER: AssetKind.SYNTH,
}


class Asset(NamedTuple):
    """
    Asset is used to identify a blockchain asset in the cross-chain environment.
    It has chain, symbol, and contract fields.
    """

    chain: str
    """
    The blockchain identifier. E.g. 'BNB', 'ETH', 'BTC', etc.
    This field has type str. Be careful to not confuse this with the Chain object.
    """
    # fixme: should we make chain type as Chain enum?

    symbol: str
    """The asset symbol. E.g. 'RUNE', 'BTC', 'ETH', etc."""
    contract: str = ''
    """The contract address of the asset. E.g. '0x1234...5678'. Default is empty."""
    kind: AssetKind = AssetKind.NATIVE
    """Asset kind. Default is native (L1 asset). Possible values: native, synth, trade, derived, secured."""

    @property
    def is_native(self):
        """
        Check if the asset is a native (L1) asset.
        """
        return self.kind == AssetKind.NATIVE

    @property
    def chain_enum(self) -> Chain:
        """
        Returns chain field in form of Chain enumeration instance

        :return: Chain
        """
        return Chain(self.chain)

    @property
    def is_synth(self):
        """
        Check if the asset is a synth asset.
        """
        return self.kind == AssetKind.SYNTH

    @property
    def synth(self):
        """
        Check if the asset is a synth asset. Same as is_synth.
        It is here for compatibility with the old version of the Asset class.
        """
        return self.is_synth

    @property
    def is_trade(self):
        """
        Check if the asset is a trade asset.
        """
        return self.kind == AssetKind.TRADE

    @property
    def is_secured(self):
        """
        Check if the asset is a secured asset.
        """
        return self.kind == AssetKind.SECURED

    @property
    def is_derived(self):
        """
        Check if the asset is a derived asset.
        """
        return self.kind == AssetKind.DERIVED

    @property
    def is_valid(self):
        """
        Check if the asset is valid. An asset is valid if it has both chain and symbol.
        If the asset is a derived asset, it must be a THORChain asset.
        """
        if not self.chain or not self.symbol:
            return False

        if self.is_derived and self.chain != Chain.THORChain.value:
            return False

        return True

    @property
    def delimiter(self):
        """
        Get the delimiter based on whether the asset is a synth or not.
        Synth assets use '/' as delimiter (BTC/BTC) while non-synth (native) assets use '.' as delimiter (THOR.RUNE).
        Trade assets use '~' as delimiter (BTC~BTC).
        """
        if self.is_synth:
            return SYNTH_DELIMITER
        elif self.is_trade:
            return TRADE_DELIMITER
        elif self.is_secured:
            return SECURED_DELIMITER
        else:
            return NATIVE_DELIMITER

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
        components = input_str.split('-', maxsplit=1)
        if len(components) == 2:
            return components
        elif len(components) == 1:
            return input_str, ''
        else:
            raise ValueError(f'Invalid input string: {input_str}')

    @classmethod
    def from_string(cls, s) -> Optional['Asset']:
        """
        Create an Asset object by parsing the input string.
        If the input string is already an Asset object, it will be returned as is.
        The format of the input string should be "CHAIN.SYMBOL-CONTRACT".
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
        if not s:
            raise ValueError('Asset string cannot be empty.')

        kind = AssetKind.recognize(s)

        data = s.split(kind.delimiter, 1)
        n = len(data)
        if n == 1:
            if symbol := data[0]:
                if not symbol:
                    raise ValueError(f'Asset symbol cannot be empty. You passed "{s}"')
                return cls(symbol, symbol)
        elif n == 2:
            chain, name_part = data
            chain = chain.strip()
            if not chain:
                raise ValueError(f'Asset chain cannot be empty. You passed "{s}"')

            name_part = name_part.strip()
            if not name_part:
                raise ValueError(f'Asset name cannot be empty. You passed "{s}"')

            if "." in name_part:
                raise ValueError(f'Invalid extra symbol "." in "{name_part}"')
            name, tag = cls.get_name_and_contract(name_part)

            if kind is AssetKind.NATIVE and chain.upper() == Chain.THORChain.value:
                # Looks like THOR.BTC
                kind = AssetKind.DERIVED

            return cls(chain, name, tag, kind)

    @classmethod
    def from_string_no_exc(cls, s) -> Optional['Asset']:
        """
        Create an Asset object by parsing the input string.
        Return None if input string is invalid. Does not raise an exception.

        :param s: The input string to parse
        :return: An Asset object if the input string is valid, otherwise None
        :rtype: Optional[Asset]
        """
        with suppress(ValueError):
            return cls.from_string(s)
        return None

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
        return self._replace(kind=AssetKind.NATIVE)

    @property
    def as_synth(self):
        """
        Get a synth copy of the asset object. Synth assets use '/' as delimiter (BTC/BTC).

        :return: A synth version of the asset.
        """
        return self._replace(kind=AssetKind.SYNTH)

    @property
    def as_trade(self):
        """
        Get a trade copy of the asset object. Trade assets use '~' as delimiter (BTC~BTC).

        :return: A trade version of the asset.
        """
        return self._replace(kind=AssetKind.TRADE)

    @property
    def as_secured(self):
        """
        Get a secured copy of the asset object. Secured assets use '-' as delimiter (ETH-ETH).

        :return: A secured version of the asset.
        """
        return self._replace(kind=AssetKind.SECURED)

    @property
    def as_derived(self):
        """
        Return a "derived"-type copy of the asset object.
        Note, that chain will be set as THORChain.

        :return: Asset
        """
        return self._replace(kind=AssetKind.DERIVED, chain=Chain.THORChain.value)

    @property
    def is_rune_native(self):
        """
        Check if the asset is a native RUNE asset.

        :return:
        """
        return self.chain == Chain.THORChain.value and self.symbol == 'RUNE'

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

    @classmethod
    def dimensionless(cls):
        """
        Get a dimensionless asset, which is an asset with empty chain and symbol.

        :return: A dimensionless Asset object.
        """

        return cls(Chain.THORChain.value, '', '', AssetKind.NATIVE)

    @property
    def is_dimensionless(self):
        """
        Check if the asset is dimensionless, which means it has an empty chain and symbol.

        :return: True if the asset is dimensionless, otherwise False.
        """
        return not self.symbol


AssetBTC = Asset.from_string('BTC.BTC')
"""Bitcoin asset on the Bitcoin network."""

AssetETH = Asset.from_string('ETH.ETH')
"""Ethereum asset on the Ethereum network."""

AssetBSC = Asset.from_string('BSC.BNB')
"""Binance Coin asset on the Binance Smart Chain."""

AssetBCH = Asset.from_string('BCH.BCH')
"""Bitcoin Cash asset on the Bitcoin Cash network."""

AssetLTC = Asset.from_string('LTC.LTC')
"""Litecoin asset on the Litecoin network."""

AssetDOGE = Asset.from_string('DOGE.DOGE')
"""Dogecoin asset on the Dogecoin network."""

AssetAVAX = Asset.from_string('AVAX.AVAX')
"""Avalanche asset on the Avalanche C-Chain."""

AssetAEth = Asset.from_string('ARB.ETH')
"""Arbitrum Ethereum asset on the Arbitrum network."""

AssetRUNE = Asset.from_string('THOR.RUNE')
"""THORChain RUNE asset on the THORChain network."""

AssetATOM = Asset.from_string('GAIA.ATOM')
"""Cosmos Atom asset on the Cosmos network."""

AssetCACAO = Asset.from_string('MAYA.CACAO')
"""Maya Cacao asset on the Maya network."""

AssetDASH = Asset.from_string('DASH.DASH')
"""Dash asset on the Dash network."""

AssetKUJI = Asset.from_string('KUJI.KUJI')
"""Kujira asset on the Kujira network."""

AssetBaseETH = Asset.from_string('BASE.ETH')
"""Base Ethereum asset on the Base network."""

AssetTCY = Asset.from_string("THOR.TCY")
"""TCY asset on the THORChain network."""

AssetRUJI = Asset.from_string("THOR.RUJI")
"""Rujira asset on the THORChain network."""

AssetXRP = Asset.from_string('XRP.XRP')
"""XRP Ripple asset on the XRP network."""

AssetSOL = Asset.from_string('SOL.SOL')
"""Solana asset on the Solana network."""


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
    elif chain == Chain.Kujira:
        return AssetKUJI
    elif chain == Chain.Arbitrum:
        return AssetAEth
    elif chain == Chain.Base:
        return AssetBaseETH
    elif chain == Chain.Ripple:
        return AssetXRP
    elif chain == Chain.Solana:
        return AssetSOL

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
    """Bitcoin asset"""

    ETH = AssetETH
    """Ethereum asset"""

    BSC = AssetBSC
    """Binance Coin asset in the Binance Smart Chain"""

    BCH = AssetBCH
    """Bitcoin Cash asset"""

    LTC = AssetLTC
    """Litecoin asset"""

    DOGE = AssetDOGE
    """Dogecoin asset"""

    AVAX = AssetAVAX
    """Avalanche asset in the Avalanche C-Chain"""

    AEth = AssetAEth
    """Arbitrum Ethereum asset"""

    RUNE = AssetRUNE
    """THORChain asset"""

    ATOM = AssetATOM
    """Cosmos Atom asset"""

    CACAO = AssetCACAO
    """Maya Cacao asset"""

    DASH = AssetDASH
    """Dash asset"""

    KUJI = AssetKUJI
    """Kujira asset"""

    BASE_ETH = AssetBaseETH
    """Base Ethereum asset"""

    XRP = AssetXRP
    """XRP Ripple asset"""

    SOL = AssetSOL
    """Solana asset"""

    SHORT_CODES = {
        'a': AssetAVAX,
        'b': AssetBTC,
        'c': AssetBCH,
        'd': AssetDOGE,
        'e': AssetETH,
        'g': AssetATOM,
        'l': AssetLTC,
        's': AssetBSC,
        'r': AssetRUNE,
        'f': AssetBaseETH,
        'x': AssetXRP,
    }
    """
    THORChain short codes for common assets.
    todo: move them to the THORChain package
    """

    INVERTED_SHORT_CODES = {v: k for k, v in SHORT_CODES.items()}


def get_short_code(asset: Union[Asset, str]) -> str:
    """
    Get the short code for the specified asset.

    :param asset: The asset to get the short code for
    :return: The short code for the asset
    """
    asset = Asset.from_string(asset)
    return CommonAssets.INVERTED_SHORT_CODES.get(asset, '')
