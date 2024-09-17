from typing import Optional

# from cosmpy.aerial.client import Coin as CosmosCoin
from cosmpy.aerial.tx import Transaction, SigningCfg
from cosmpy.crypto.keypairs import PublicKey

from xchainpy2_cosmos.utils import convert_address_for_msg
from xchainpy2_utils import NetworkType, CryptoAmount, Amount, RUNE_DECIMAL, Asset, AssetRUNE
from .const import DEPOSIT_GAS_LIMIT_VALUE, DENOM_RUNE_NATIVE
from .proto import THORCoin, THORAsset, MsgSend, MsgDeposit, CosmosCoin


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


def crypto_amount_to_msg_coin(a: CryptoAmount) -> THORCoin:
    asset = THORAsset(
        chain=a.asset.chain,
        symbol=a.asset.full_symbol,
        ticker=a.asset.symbol,
        synth=a.asset.synth,
        trade=a.asset.is_trade,
    )
    return THORCoin(
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
        MsgDeposit(coins=coins, memo=memo, signer=convert_address_for_msg(signer_public_key, prefix))
    )

    tx = tx.seal(
        SigningCfg.direct(signer_public_key, sequence_num),
        fee=fee,
        gas_limit=int(gas_limit),
        memo=memo
    )

    return tx


def build_transfer_tx_draft(what: CryptoAmount, denom: str, sender: str, recipient: str,
                            prefix: str) -> Transaction:
    tx = Transaction()

    tx.add_message(
        msg=MsgSend(
            from_address=convert_address_for_msg(sender, prefix),
            to_address=convert_address_for_msg(recipient, prefix),
            amount=[
                CosmosCoin(amount=str(what.amount.internal_amount), denom=denom)
            ],
        )
    )
    return tx


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
