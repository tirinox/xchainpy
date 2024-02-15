from typing import NamedTuple, Optional, Union

from .chain import Chain
from .util import XChainProtocol

SYNTH_DELIMITER = '/'
NON_SYNTH_DELIMITER = '.'


def get_delimiter(synth: bool):
    return SYNTH_DELIMITER if synth else NON_SYNTH_DELIMITER


class Asset(NamedTuple):
    chain: str
    symbol: str
    contract: str = ''
    synth: bool = False

    @property
    def is_valid(self):
        return self.chain and self.symbol

    @property
    def delimiter(self):
        return SYNTH_DELIMITER if self.synth else NON_SYNTH_DELIMITER

    def __str__(self):
        s = f'{self.chain}{self.delimiter}{self.symbol}'
        if self.contract:
            s += f'-{self.contract}'
        return s

    @staticmethod
    def get_name_and_contract(input_str):
        components = input_str.split('-', maxsplit=2)
        if len(components) == 2:
            return components
        else:
            return input_str, ''

    @classmethod
    def from_string(cls, s) -> Optional['Asset']:
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
        a = cls.from_string(s)
        if a is None:
            raise ValueError(f'Invalid asset string: {s}')
        return a

    @classmethod
    def automatic(cls, x) -> Optional['Asset']:
        if isinstance(x, str):
            return cls.from_string(x)
        elif isinstance(x, Asset):
            return x

    @property
    def as_native(self):
        # noinspection PyArgumentEqualDefault
        return self._replace(synth=False)

    @property
    def as_synth(self):
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
        return self.symbol

    @property
    def full_symbol(self):
        return f"{self.symbol}-{self.contract}" if self.contract else self.symbol

    @classmethod
    def dummy(cls):
        return cls('', '')

    @property
    def is_gas(self):
        return is_gas_asset(self)

    def upper(self):
        return self._replace(
            symbol=self.symbol.upper(),
            contract=self.contract.upper(),
            chain=self.chain.upper() if self.chain else self.chain
        )

    def __eq__(self, other: 'Asset'):
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
AssetRUNE = Asset.from_string('THOR.RUNE')
AssetATOM = Asset.from_string('GAIA.ATOM')
AssetCACAO = Asset.from_string('MAYA.CACAO')
AssetDASH = Asset.from_string('DASH.DASH')


def get_chain_gas_asset(chain: Union[Chain, str]) -> Asset:
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
    # todo: should we check for synth?
    return get_chain_gas_asset(Chain(asset.chain)) == asset
