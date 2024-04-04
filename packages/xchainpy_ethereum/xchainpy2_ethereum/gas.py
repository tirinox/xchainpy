from typing import Optional, NamedTuple

from xchainpy2_client import FeeOption


class GasOptions(NamedTuple):
    fee_option: Optional[FeeOption] = None
    gas_price: Optional[int] = None
    max_fee_per_gas: Optional[int] = None
    max_priority_fee_per_gas: Optional[int] = None
    gas_limit: Optional[int] = None

    @classmethod
    def automatic(cls, fee_option: FeeOption):
        return cls(fee_option=fee_option)

    @classmethod
    def legacy(cls, gas_price: int, gas_limit: int):
        return cls(gas_price=gas_price, gas_limit=gas_limit)

    @classmethod
    def eip1559(cls, max_fee_per_gas: int, max_priority_fee_per_gas: int, gas_limit: int):
        return cls(max_fee_per_gas=max_fee_per_gas,
                   max_priority_fee_per_gas=max_priority_fee_per_gas,
                   gas_limit=gas_limit)

    def validate(self):
        assert self.fee_option or self.gas_price or (self.max_fee_per_gas and self.max_priority_fee_per_gas), \
            "Either fee_option or gas_price or (max_fee_per_gas and max_priority_fee_per_gas) must be set"


class GasLimits(NamedTuple):
    approve_gas_limit: int
    transfer_gas_asset_gas_limit: int
    transfer_token_gas_limit: int
    gas_price: int

    @classmethod
    def default(cls):
        return cls(
            200000,
            23000,
            100000,
            30 * 10 ** 9,
        )
