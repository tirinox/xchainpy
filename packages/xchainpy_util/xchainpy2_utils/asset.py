from typing import NamedTuple, Optional

from .consts import XChainProtocol

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
        if n < 1:
            return None
        elif n == 1:
            return cls(data[0], data[0])
        elif n == 2:
            name, tag = cls.get_name_and_contract(data[1])
            return cls(data[0], name, tag, is_synth)

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


AssetBTC = Asset('BTC', 'BTC', 'BTC', False)
AssetETH = Asset('ETH', 'ETH', 'ETH', False)
AssetBNB = Asset('BNB', 'BNB', 'BNB', False)
AssetBCH = Asset('BCH', 'BCH', 'BCH', False)
AssetLTC = Asset('LTC', 'LTC', 'LTC', False)
AssetDOGE = Asset('DOGE', 'DOGE', 'DOGE', False)
AssetAVAX = Asset('AVAX', 'AVAX', 'AVAX', False)
AssetRUNE = Asset('THOR', 'RUNE', 'RUNE', False)
AssetATOM = Asset('GAIA', 'ATOM', 'ATOM', False)
AssetCACAO = Asset('MAYA', 'CACAO', 'CACAO', False)
