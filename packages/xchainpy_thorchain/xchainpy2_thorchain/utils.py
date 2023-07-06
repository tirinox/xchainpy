from datetime import datetime
from typing import Optional, List

from cosmpy.aerial.client import Coin as CosmosCoin
from cosmpy.aerial.tx import Transaction, SigningCfg
from cosmpy.crypto.address import Address
from cosmpy.crypto.keypairs import PublicKey

from xchainpy2_client import XcTx, TxType, TxTo, TxFrom
from xchainpy2_cosmos import TxLog
from xchainpy2_utils import NetworkType, CryptoAmount, Amount, RUNE_DECIMAL, Asset, Denomination
from .const import DEPOSIT_GAS_LIMIT_VALUE
from .proto.thorchain.v1.common.common_pb2 import Coin, Asset as THORAsset
from .proto.thorchain.v1.x.thorchain.types.msg_deposit_pb2 import MsgDeposit


def get_thor_address_prefix(network: NetworkType) -> str:
    """
    Get address prefix based on the network.
    :param network:
    :return: string address prefix
    """
    if network == NetworkType.TESTNET:
        return 'tthor'
    elif network == NetworkType.STAGENET:
        return 'sthor'
    elif network == NetworkType.MAINNET:
        return 'thor'
    else:
        raise ValueError('Invalid network')


def convert_coin_to_crypto_amount(coin: CosmosCoin, decimals=RUNE_DECIMAL) -> CryptoAmount:
    asset = Asset.from_string(f'THOR.{coin.denom.upper()}')
    return CryptoAmount(
        amount=Amount.from_base(coin.amount, decimals),
        asset=asset
    )


def crypto_amount_to_msg_coin(a: CryptoAmount) -> Coin:
    asset = THORAsset(
        chain=a.asset.chain,
        symbol=a.asset.full_symbol,
        ticker=a.asset.symbol,
        synth=a.asset.synth
    )
    return Coin(
        asset=asset,
        amount=str(a.amount.as_base.amount), decimals=a.amount.decimals
    )


def build_deposit_tx_unsigned(
        what: CryptoAmount,
        memo: str,
        signer_public_key: PublicKey,
        sequence_num: int,
        prefix: str = 'thor',
        fee=None,
        gas_limit=DEPOSIT_GAS_LIMIT_VALUE,
        second_asset: Optional[CryptoAmount] = None) -> Transaction:
    coins = [
        crypto_amount_to_msg_coin(what)
    ]
    if second_asset is not None:
        coins.append(crypto_amount_to_msg_coin(second_asset))

    tx = Transaction()
    tx.add_message(
        MsgDeposit(coins=coins, memo=memo, signer=bytes(Address(signer_public_key, prefix)))
    )

    tx = tx.seal(
        SigningCfg.direct(signer_public_key, sequence_num),
        fee=fee,
        gas_limit=int(gas_limit),
        memo=memo
    )

    return tx


class TransferDatum(NamedTuple):
    sender: str
    recipient: str
    amount: Amount


def get_deposit_tx_from_logs(logs: List[TxLog],
                             address: str,
                             sender_asset: Optional[Asset],
                             receiver_address: Optional[Address],
                             decimals=8,
                             denom='rune') -> XcTx:
    if not logs:
        raise ValueError('No logs available')

    events = logs[0].events
    if not events:
        raise ValueError('No events available in logs')

    transfer_data_list = []
    sender, recipient, amount = None, None, None
    for event in events:
        if event.type == 'transfer':
            for i, attribute in enumerate(event.attributes):
                if attribute.key == 'sender':
                    sender = attribute.value
                elif attribute.key == 'recipient':
                    recipient = attribute.value
                elif attribute.key == 'amount':
                    value = attribute.value.replace(denom, '')
                    amount = Amount.from_base(value, decimals)

                # ready to append
                if sender and recipient and amount:
                    transfer_data_list.append(TransferDatum(sender, recipient, amount))
                    # reset
                    sender, recipient, amount = None, None, None

    transfer_data_list = [
        data for data in transfer_data_list
        if data.sender == address or data.recipient == address
    ]

    from_txs, to_txs = [], []

    for data in transfer_data_list:
        to_txs.append(TxTo(
            data.recipient,
            data.amount,
            receiver_address
        ))
        from_txs.append(TxFrom(
            data.sender, '',
            data.amount,
            sender_asset
        ))

    return XcTx(Asset.dummy(), from_txs, to_txs, datetime.fromtimestamp(0), TxType.TRANSFER, '')
