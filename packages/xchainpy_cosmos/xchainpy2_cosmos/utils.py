from typing import Optional, List, Tuple


from cosmpy.crypto.address import Address

from xchainpy2_client import XcTx, TxType, TokenTransfer
from xchainpy2_utils import Asset, AssetATOM, Chain, Amount, key_attr_getter, parse_iso_date
from .const import COSMOS_DENOM
from .models import TxLoadException, load_logs, TxLog


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


def get_asset(denom: str, native_denom=COSMOS_DENOM, native_asset=AssetATOM) -> Optional[Asset]:
    """
    Get Asset from denomination - currently `ATOM` supported only
    :param denom:
    :param native_asset:
    :param native_denom:
    :return: The asset of the given denomination.
    """
    if denom == native_denom:
        return native_asset

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


def get_coin_amount(coins, decimals) -> Amount:
    return sum(
        (Amount.from_base(int(key_attr_getter(coin, 'amount')), decimals) for coin in coins),
        Amount.from_base(0, decimals)
    )


def get_coins_by_asset(coins, search_asset: Asset, native_denom: str, native_asset: Asset):
    return [
        coin for coin in coins
        if get_asset(key_attr_getter(coin, 'denom'), native_denom, native_asset) == search_asset
    ]


def parse_transfer_log(log: TxLog, decimals, filter_address, native_denom: str, native_asset: Asset) \
        -> List[TokenTransfer]:
    transfer_data_list = []
    sender, recipient, amount, asset = None, None, None, None
    for event in log.events:
        if event.type == 'transfer':
            for i, attribute in enumerate(event.attributes):
                if attribute.key == 'sender':
                    sender = attribute.value
                elif attribute.key == 'recipient':
                    recipient = attribute.value
                elif attribute.key == 'amount':
                    amount_int, asset = parse_cosmos_amount(attribute.value)
                    amount = Amount.from_base(amount_int, decimals)
                    if asset == native_denom:
                        asset = native_asset
                    else:
                        asset = Asset.from_string(asset.upper())

                # ready to append
                if sender and recipient and amount and asset:
                    transfer_data_list.append(
                        TokenTransfer(
                            sender, recipient, amount, asset,
                            tx_hash='', outbound=(sender == filter_address)
                        ))

                    sender, recipient, amount, asset = None, None, None, None  # reset

    if filter_address:
        transfer_data_list = [
            data for data in transfer_data_list
            if data.from_address == filter_address or data.to_address == filter_address
        ]

    return transfer_data_list


def parse_tx_response_json(j: dict, tx_id: str, address: str, decimals: int,
                           native_denom: str, native_asset: Asset) -> XcTx:
    response = j.get('tx_response')
    if not response:
        raise TxLoadException(f'Failed to get transaction logs (tx-hash: ${tx_id}): no tx_response')

    code = response.get('code')
    is_successful = code == 0
    if not is_successful:
        raise TxLoadException(f'Code is not 0 ({code}) for tx-hash: ${tx_id}')

    messages = j['tx']['body']['messages']

    if len(messages) > 1:
        raise TxLoadException(f'Multiple messages are not supported yet (tx-hash: ${tx_id})')
    elif not messages:
        raise TxLoadException(f'No messages found (tx-hash: ${tx_id})')

    address = address or messages[0].get('signer') or messages[0].get('from_address')

    logs = load_logs(response.get('logs'))
    if not logs:
        raise TxLoadException(f'Failed to get transaction logs (tx-hash: ${tx_id})')

    if len(logs) > 1:
        raise TxLoadException(f'Multiple logs are not supported yet (tx-hash: ${tx_id})')

    log = logs[0]

    transfers_events = log.find_events('transfer')
    message_event = log.find_event('message')
    if not transfers_events and not message_event:
        raise TxLoadException(f'Invalid transaction data, no transfer/no message (tx-hash: ${tx_id})')

    memo = ''
    if (tx_j := j.get('tx')) and (body := tx_j.get('body')):
        memo = body['memo']

    tx_date = parse_iso_date(response['timestamp'])
    tx_hash = response['txhash']
    height = int(response['height'])

    transfers = parse_transfer_log(log, decimals, address, native_denom, native_asset)

    return XcTx(
        asset=transfers[0].asset if transfers else None,
        transfers=transfers,
        date=tx_date,
        type=TxType.TRANSFER,
        hash=tx_hash,
        height=height,
        memo=memo,
        original=j,
    )


def parse_cosmos_amount(amount: str) -> Tuple[int, str]:
    """
    Parse COSMOS amount
    into integer amount and string denomination
    :param amount: a string with format "123asset", like "100rune"
    :return: (int, str)
    """
    for i, char in enumerate(amount):
        if not char.isdigit():
            pos = i
            break
    else:
        raise ValueError(f'Invalid format: {amount!r} Must be like "10rune"')

    return (
        int(amount[:pos]),
        amount[pos:]
    )


def parse_cosmos_amounts(value: str) -> List[Tuple[int, str]]:
    """
    Parse COSMOS amounts from string like "1234rune,1234bnb"
    :param value: Cosmos SDK amount string
    :return: List of (value, asset) pairs
    """
    if not value:
        return []
    items = value.split(',')
    return [parse_cosmos_amount(item.strip()) for item in items]


def convert_address_for_msg(address, prefix: str) -> bytes:
    return bytes(Address(address, prefix))
