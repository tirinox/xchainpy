from xchainpy2_utils import Chain, is_gas_asset
from .consts import THOR_BASIS_POINT_MAX, THOR_DIVIDER_INV, THOR_DIVIDER


def bp_to_float(bp):
    return int(bp) / THOR_BASIS_POINT_MAX


def bp_to_percent(bp):
    return bp_to_float(bp) * 100.0


def thor_to_float(x) -> float:
    return int(x) * THOR_DIVIDER_INV


def float_to_thor(x: float) -> int:
    return int(x * THOR_DIVIDER)


def is_erc20_asset(asset):
    return Chain(asset.chain).is_evm and not is_gas_asset(asset)
