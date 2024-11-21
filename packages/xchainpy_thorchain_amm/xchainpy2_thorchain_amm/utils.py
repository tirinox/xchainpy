from xchainpy2_utils import Chain, is_gas_asset, Asset
from .consts import THOR_BASIS_POINT_MAX, THOR_DIVIDER_INV, THOR_DIVIDER


def bp_to_float(bp):
    """
    Convert basis points to float in range [0, 1]
    :param bp: Basis points (int or str), 0..THOR_BASIS_POINT_MAX
    :return: float
    """
    return int(bp) / THOR_BASIS_POINT_MAX


def bp_to_percent(bp):
    """
    Convert basis points to percentage in range [0, 100]
    :param bp: Basis points (int or str), 0..THOR_BASIS_POINT_MAX
    :return: Percentage (float 0..100%)
    """
    return bp_to_float(bp) * 100.0


def thor_to_float(x) -> float:
    return int(x) * THOR_DIVIDER_INV


def float_to_thor(x: float) -> int:
    return int(x * THOR_DIVIDER)


def is_erc20_asset(asset: Asset):
    """
    Naive check if the asset is an ERC20 asset.
    Basically, the asset is an ERC20 asset if its chain is recognized as an EVM chain, and it is not a gas asset.
    :param asset: Asset to check
    :return: bool
    """
    return Chain(asset.chain).is_evm and not is_gas_asset(asset)
