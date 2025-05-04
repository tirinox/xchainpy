from decimal import Decimal

from xchainpy2_thorchain_query.models import InboundDetail
from xchainpy2_utils import CryptoAmount, Amount, CACAO_DECIMAL, AssetCACAO, Asset, AssetRUNE, RUNE_DECIMAL, Chain, \
    AssetBTC, AssetDOGE, AssetLTC, AssetBCH, AssetBNB, AssetATOM, get_chain_gas_asset, ETH_DECIMALS

try:
    from xchainpy2_mayachain import DEFAULT_CACAO_NETWORK_FEE
except ModuleNotFoundError:
    DEFAULT_CACAO_NETWORK_FEE = CryptoAmount(Amount.from_asset(Decimal("0.5"), CACAO_DECIMAL), AssetCACAO)

try:
    from xchainpy2_thorchain import DEFAULT_RUNE_NETWORK_FEE
except ModuleNotFoundError:
    DEFAULT_RUNE_NETWORK_FEE = CryptoAmount(Amount.from_asset(Decimal("0.02"), RUNE_DECIMAL), AssetRUNE)


def calc_network_fee(asset: Asset, inbound: InboundDetail,
                     base_asset: Asset = AssetRUNE) -> CryptoAmount:
    """
    Works out the required inbound fee based on the chain.
    https://dev.thorchain.org/thorchain-dev/thorchain-and-fees#fee-calcuation-by-chain

    :param base_asset:
    :param asset: source asset
    :param inbound: inbound detail to get gas rates
    :return: amount of network fee
    """
    if asset.synth:
        if base_asset == AssetRUNE:
            return DEFAULT_RUNE_NETWORK_FEE
        elif base_asset == AssetCACAO:
            return DEFAULT_CACAO_NETWORK_FEE
        else:
            raise ValueError("Invalid Base Asset, expected RUNE or CACAO")

    if asset.chain == Chain.Bitcoin.value:
        return CryptoAmount(Amount.from_base(inbound.gas_rate * inbound.outbound_tx_size), AssetBTC)
    elif asset.chain == Chain.BitcoinCash.value:
        return CryptoAmount(Amount.from_base(inbound.gas_rate * inbound.outbound_tx_size), AssetBCH)
    elif asset.chain == Chain.Litecoin.value:
        return CryptoAmount(Amount.from_base(inbound.gas_rate * inbound.outbound_tx_size), AssetLTC)
    elif asset.chain == Chain.Doge.value:
        return CryptoAmount(Amount.from_base(inbound.gas_rate * inbound.outbound_tx_size), AssetDOGE)
    elif asset.chain == Chain.Binance.value:
        return CryptoAmount(Amount.from_base(inbound.gas_rate), AssetBNB)
    elif Chain(asset.chain).is_evm:
        gas_asset = get_chain_gas_asset(Chain(asset.chain))
        decimals = ETH_DECIMALS
        gas_rate_in_gwei = Decimal(inbound.gas_rate)
        gas_rate_in_wei = Amount.from_base(gas_rate_in_gwei * Decimal(10 ** 9), decimals)
        if asset == gas_asset:
            return CryptoAmount(Amount.from_base(gas_rate_in_wei * 23000), gas_asset)
        else:
            return CryptoAmount(Amount.from_base(gas_rate_in_wei * 70000), gas_asset)
    elif asset.chain == Chain.Cosmos.value:
        return CryptoAmount(Amount.from_base(inbound.gas_rate), AssetATOM)
    elif asset.chain == Chain.THORChain.value:
        return DEFAULT_RUNE_NETWORK_FEE
    elif asset.chain == Chain.Maya.value:
        return DEFAULT_CACAO_NETWORK_FEE
    else:
        raise ValueError(f"Could not calculate inbound fee for {asset.chain} Chain")


def calc_outbound_fee(asset: Asset, inbound: InboundDetail, base_asset=AssetRUNE) -> CryptoAmount:
    """
    Works out the required outbound fee based on the chain.

    :param asset: Asset to send
    :param inbound: Inbound detail for specific chain
    :param base_asset: Rune or Cacao depending on the protocol
    :return: CryptoAmount of outbound fee
    """
    if asset.synth:
        if base_asset == AssetRUNE:
            return DEFAULT_RUNE_NETWORK_FEE
        elif base_asset == AssetCACAO:
            return DEFAULT_CACAO_NETWORK_FEE
        else:
            raise ValueError("Invalid Base Asset, expected RUNE or CACAO")

    if asset.chain == Chain.Bitcoin.value:
        return CryptoAmount(Amount.from_base(inbound.outbound_fee), AssetBTC)
    elif asset.chain == Chain.BitcoinCash.value:
        return CryptoAmount(Amount.from_base(inbound.outbound_fee), AssetBCH)
    elif asset.chain == Chain.Litecoin.value:
        return CryptoAmount(Amount.from_base(inbound.outbound_fee), AssetLTC)
    elif asset.chain == Chain.Doge.value:
        return CryptoAmount(Amount.from_base(inbound.outbound_fee), AssetDOGE)
    elif asset.chain == Chain.Binance.value:
        return CryptoAmount(Amount.from_base(inbound.outbound_fee), AssetBNB)
    elif Chain(asset.chain).is_evm:
        gas_asset = get_chain_gas_asset(Chain(asset.chain))
        decimals = ETH_DECIMALS
        wei = Decimal(inbound.outbound_fee) * Decimal(10 ** 9)
        return CryptoAmount(Amount.from_base(wei, decimals), gas_asset)
    elif asset.chain == Chain.Cosmos.value:
        return CryptoAmount(Amount.from_base(inbound.outbound_fee), AssetATOM)
    elif asset.chain == Chain.THORChain.value:
        return DEFAULT_RUNE_NETWORK_FEE
    elif asset.chain == Chain.Maya.value:
        return DEFAULT_CACAO_NETWORK_FEE
    else:
        raise ValueError(f"Could not calculate outbound fee for {asset.chain} chain")
