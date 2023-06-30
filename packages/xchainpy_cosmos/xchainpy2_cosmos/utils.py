from datetime import datetime
from typing import Optional, List

from xchainpy2_client import XcTx, TxFrom, TxType
from xchainpy2_utils import Asset, AssetATOM, Chain, Amount, key_attr_getter
from .const import COSMOS_DENOM, COSMOS_DECIMAL
from .models import TxResponse


def is_msg_multi_send(msg):
    return key_attr_getter(msg, 'inputs') and key_attr_getter(msg, 'outputs')


def is_msg_send(msg):
    return key_attr_getter(msg, 'from_address') and \
        key_attr_getter(msg, 'to_address') and \
        key_attr_getter(msg, 'amount')


def get_denom(asset: Asset) -> str:
    """
    Get denomination from Asset - currently `ATOM` supported only
    :param asset:
    :return: The denomination of the given asset.
    """
    if asset == AssetATOM:
        return COSMOS_DENOM
    return ''


def get_asset(denom: str) -> Optional[Asset]:
    """
    Get Asset from denomination - currently `ATOM` supported only
    :param denom:
    :return: The asset of the given denomination.
    """
    if denom == COSMOS_DENOM:
        return AssetATOM

    # IBC assets
    if denom.startswith('ibc/'):
        # Note: Don't use `assetFromString` here, it will interpret `/` as synth
        return Asset(
            Chain.Cosmos.value,
            symbol=denom.split('/', maxsplit=2)[1],
            # TODO (xchain-contributors)
            # Get readable ticker for IBC assets from denom #600 https://github.com/xchainjs/xchainjs-lib/issues/600
            # At the meantime ticker will be empty
            contract='',
            synth=False
        )

    return None


def get_coin_amount(coins) -> Amount:
    return sum(
        (Amount.from_base(int(key_attr_getter(coin, 'amount')), COSMOS_DECIMAL) for coin in coins),
        Amount.from_base(0, COSMOS_DECIMAL)
    )


def get_coins_by_asset(coins, asset: Asset):
    return [
        coin for coin in coins
        if get_asset(key_attr_getter(coin, 'denom')) == asset
    ]


def parse_tx_response(tx: TxResponse, asset: Asset) -> XcTx:
    messages = tx.tx['body']['messages']
    from_txs = {}
    to_txs = {}

    for msg in messages:
        if is_msg_send(msg):
            coins = get_coins_by_asset(key_attr_getter(msg, 'amount'), asset)
            amount = get_coin_amount(coins)

            from_a = key_attr_getter(msg, 'from_address')
            from_already = from_txs.get(from_a)
            if from_already:
                from_txs[from_a] = from_already._replace(
                    amount=from_already.amount + amount
                )
            else:
                from_txs[from_a] = TxFrom(
                    from_address=from_a,
                    from_tx_hash=tx.txhash,
                    amount=amount,
                )

            to_a = key_attr_getter(msg, 'to_address')
            to_already = to_txs.get(to_a)
            if to_already:
                to_txs[to_a] = to_already._replace(
                    amount=to_already.amount + amount
                )
            else:
                to_txs[to_a] = TxFrom(
                    from_address=to_a,
                    from_tx_hash=tx.txhash,
                    amount=amount,
                )

    try:
        dt = datetime.fromtimestamp(int(tx.timestamp))
    except ValueError:
        dt = datetime.strptime(tx.timestamp, "%Y-%m-%dT%H:%M:%SZ")

    return XcTx(
        asset=asset,
        from_txs=list(from_txs.values()),
        to_txs=list(to_txs.values()),
        date=dt,
        type=TxType.TRANSFER if from_txs or to_txs else TxType.UNKNOWN,
        hash=tx.txhash,
    )


def get_txs_from_history(txs: TxResponse, asset: Asset) -> List[XcTx]:
    # order list to have latest txs first in list
    txs = sorted(txs, key=lambda tx: tx.timestamp, reverse=True)
    return [parse_tx_response(tx, asset) for tx in txs]


async def build_deposit_tx():
    ...
