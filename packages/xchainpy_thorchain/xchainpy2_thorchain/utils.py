from typing import Optional

from cosmpy.aerial.client import Coin as CosmosCoin
from cosmpy.aerial.tx import Transaction, SigningCfg
from cosmpy.crypto.address import Address
from cosmpy.crypto.keypairs import PublicKey

from xchainpy2_utils import NetworkType, CryptoAmount, Amount, RUNE_DECIMAL, Asset
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
