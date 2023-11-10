from datetime import datetime
from typing import Optional, List, NamedTuple

from cosmpy.aerial.client import Coin as CosmosCoin
from cosmpy.aerial.tx import Transaction, SigningCfg
from cosmpy.crypto.address import Address
from cosmpy.crypto.keypairs import PublicKey

from xchainpy2_client import XcTx, TxType, TokenTransfer
from xchainpy2_cosmos import TxLog
from xchainpy2_cosmos.utils import parse_cosmos_amount
from xchainpy2_utils import NetworkType, CryptoAmount, Amount, RUNE_DECIMAL, Asset, AssetRUNE
from .const import DEPOSIT_GAS_LIMIT_VALUE, DENOM_RUNE_NATIVE
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
    asset: str


def get_deposit_tx_from_logs(logs: List[TxLog],
                             address: str,
                             sender_asset: Optional[Asset] = None,
                             receiver_address: Optional[Address] = None,
                             decimals=8,
                             denom='rune', height=0) -> XcTx:
    if not logs:
        raise ValueError('No logs available')

    events = logs[0].events
    if not events:
        raise ValueError('No events available in logs')

    transfer_data_list = []
    sender, recipient, amount, asset = None, None, None, None
    for event in events:
        if event.type == 'transfer':
            for i, attribute in enumerate(event.attributes):
                if attribute.key == 'sender':
                    sender = attribute.value
                elif attribute.key == 'recipient':
                    recipient = attribute.value
                elif attribute.key == 'amount':
                    print(attribute.value, denom)
                    amount_int, asset = parse_cosmos_amount(attribute.value)
                    amount = Amount.from_base(amount_int, decimals)

                # ready to append
                if sender and recipient and amount and asset:
                    transfer_data_list.append(TransferDatum(sender, recipient, amount, asset))
                    # reset
                    sender, recipient, amount, asset = None, None, None, None

    transfer_data_list = [
        data for data in transfer_data_list
        if data.sender == address or data.recipient == address
    ]

    transfers = []
    for data in transfer_data_list:
        asset = Asset.from_string(data.asset.upper())
        # todo: check if it is correct
        transfers.append(TokenTransfer(data.sender, data.recipient, data.amount, asset, outbound=True))
        transfers.append(TokenTransfer(data.recipient, data.sender, data.amount, asset, outbound=False))
        # to_txs.append(TxTo(
        #     data.recipient,
        #     data.amount,
        #     asset
        # ))
        # from_txs.append(TxFrom(
        #     data.sender, '',
        #     data.amount,
        #     asset
        # ))

    return XcTx(Asset.dummy(), transfers,
                datetime.fromtimestamp(0), TxType.TRANSFER, '',
                height=height)


def get_asset_from_denom(denom: str) -> Asset:
    if denom == DENOM_RUNE_NATIVE:
        return AssetRUNE
    else:
        return Asset.from_string_exc(denom.upper())
