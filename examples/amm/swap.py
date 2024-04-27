import argparse
import asyncio

from examples.common import get_phrase
from xchainpy2_thorchain_amm import THORChainAMM, Wallet
from xchainpy2_utils import CryptoAmount


def parse_arguments():
    parser = argparse.ArgumentParser(description="THORChain Automated Market Maker (AMM) Swap")

    parser.add_argument("input_amount", type=float, help="Input amount to swap")
    parser.add_argument("input_asset", type=str, help="Input asset symbol")
    parser.add_argument("output_asset", type=str, help="Output asset symbol")

    parser.add_argument("--tolerance_bps", type=float, help="Swap slip tolerance (bps)", default=500)
    parser.add_argument("--affiliate_fee_bps", type=float, help="Affiliate fee in basis points (bps)",
                        default=0)
    parser.add_argument("--affiliate_address", type=str, help="Affiliate collector address",
                        default='')
    parser.add_argument("--destination_address", type=str, help="Destination address for the swap result",
                        default='')

    parser.add_argument('--phrase', type=str,
                        help='Your secret mnemonic seed phrase. If it is empty, '
                             'the program fill try to read it from PHRASE env variable', default='')

    args = parser.parse_args()

    if not args.phrase:
        args.phrase = get_phrase()

    return args


async def main():
    # midgard = MidgardAPIClient()
    # node = THORNodeAPIClient()
    # cache = THORChainCache(midgard, node)
    # query = THORChainQuery(cache)

    phrase = get_phrase()
    wallet = Wallet(phrase)

    amm = THORChainAMM(wallet)

    args = parse_arguments()

    input_amount = args.input_amount
    input_asset = args.input_asset
    output_asset = args.output_asset
    tolerance_bps = args.tolerance_bps
    affiliate_fee_bps = args.affiliate_fee_bps
    affiliate_address = args.affiliate_address
    destination_address = args.destination_address
    decimals = None

    tx_hash = await amm.do_swap(
        input_amount=CryptoAmount.automatic(input_amount, input_asset, decimals=decimals),
        destination_asset=output_asset,
        tolerance_bps=tolerance_bps,
        affiliate_bps=affiliate_fee_bps,
        affiliate_address=affiliate_address,
        destination_address=destination_address,
    )
    print(f"Swap tx hash: {amm.get_track_url(tx_hash)}")

    await amm.close()


if __name__ == '__main__':
    asyncio.run(main())
