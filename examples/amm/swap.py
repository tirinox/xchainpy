import argparse
import asyncio

from examples.common import get_phrase
from xchainpy2_thorchain_amm import THORChainAMM, Wallet, WalletSettings
from xchainpy2_thorchain_query import THORChainQuery, THORChainCache, MidgardAPIClient
from xchainpy2_thorchain_query.thornode import THORNodeAPIClient


def parse_arguments():
    parser = argparse.ArgumentParser(description="THORChain Automated Market Maker (AMM) Swap")

    parser.add_argument("input_amount", type=float, help="Input amount to swap")
    parser.add_argument("input_asset", type=str, help="Input asset symbol")
    parser.add_argument("output_asset", type=str, help="Output asset symbol")

    parser.add_argument("--limit", type=float, help="Swap limit", default=0)
    parser.add_argument("--affiliate_fee_bps", type=float, help="Affiliate fee in basis points (bps)",
                        default=0)
    parser.add_argument("--affiliate_collector", type=str, help="Affiliate collector address",
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
    midgard = MidgardAPIClient()
    node = THORNodeAPIClient()
    cache = THORChainCache(midgard, node)
    query = THORChainQuery(cache)

    phrase = get_phrase()
    wallet = Wallet(WalletSettings.default(phrase))

    amm = THORChainAMM(query)

    args = parse_arguments()
    print(args)


if __name__ == '__main__':
    asyncio.run(main())
