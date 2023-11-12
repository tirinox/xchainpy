from typing import Optional, List

from cosmpy.aerial.client import Coin as CosmosCoin
from cosmpy.aerial.tx import Transaction, SigningCfg
from cosmpy.crypto.address import Address
from cosmpy.crypto.keypairs import PublicKey

from xchainpy2_client import TokenTransfer
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


def parse_transfer_log(log: TxLog, decimals, filter_address=None,
                       native_denom=DENOM_RUNE_NATIVE,
                       native_asset: Asset = AssetRUNE) -> List[TokenTransfer]:
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


def get_asset_from_denom(denom: str) -> Asset:
    if denom == DENOM_RUNE_NATIVE:
        return AssetRUNE
    else:
        return Asset.from_string_exc(denom.upper())


class NativeTxType:
    DEPOSIT = 'deposit'
    SEND = 'send'
    UNKNOWN = 'unknown'


def get_native_tx_type(raw_json):
    tx_type = raw_json['tx']['body']['messages'][0]['@type']
    if tx_type == "/types.MsgSend":
        return NativeTxType.SEND
    elif tx_type == "/types.MsgDeposit":
        return NativeTxType.DEPOSIT
    else:
        return NativeTxType.UNKNOWN
