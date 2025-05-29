import asyncio
import os.path
import sys

import aiofiles
import yaml

from xchainpy2_midgard.rest import ApiException
from xchainpy2_thorchain import THORChainClient, NodeURL
from xchainpy2_thorchain_amm import THORChainAMM
from xchainpy2_thorchain_query import THORChainQuery
from xchainpy2_utils import Chain, CryptoAmount, NetworkType
from xchainpy2_wallet import Wallet


class TCYBot:
    @classmethod
    async def create(cls):
        cfg = await cls.load_config()
        bot = cls(cfg)
        await bot.run_loop()

    def __init__(self, cfg):
        self.cfg = cfg
        thor = self.cfg['thor']
        phrase = thor['phrase']
        thornode = thor['node_url']
        network = thor['network_id']
        self.query = THORChainQuery.from_thornode_and_midgard(
            thornode_url=thornode,
            network=network,
        )

        self.client = THORChainClient(
            phrase=phrase,
            client_urls={
                NetworkType(network): NodeURL(thornode)
            },
            network=network,
        )

        self.wallet = Wallet.from_clients([self.client], query_api=self.query)
        self.amm = THORChainAMM(self.wallet, self.query)

    @staticmethod
    async def load_config():
        config_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__),
                                                                         "tcy_bot_config.yaml")
        async with aiofiles.open(config_file, mode='r') as f:
            content = await f.read()
        return yaml.safe_load(content)

    async def print_balances(self):
        balances = await self.wallet.get_all_balances()
        print(f"Balances of {self.wallet.get_client(Chain.THORChain).get_address()}:")
        for bc in balances.balances.values():
            for b in bc.balances:
                print(f"  {b.asset}: {b.amount}")

    async def check_possibility(self):
        try:
            r = await self.amm.query.quote_swap(
                self.buy_amount,
                self.client.get_address(),
                self.target_asset,
            )
            if not r.can_swap:
                print(f'Cannot swap: {r.errors}')
                return False

            # Check price bounds
            input_amount = self.buy_amount.amount
            output_amount = r.net_output.amount
            price = output_amount / input_amount

            print(f'Estimated net output: {r.net_output}')
            print(f"Price: {price}: {r.net_output.asset} / {self.buy_amount.asset} ")

            min_price = self.strategy.get('min_price_target_per_source_asset')
            if min_price:
                min_price = float(min_price)
                if price < min_price:
                    print(f'Price exceeds min price {min_price}. Not buying.')
                    return False

            # We can swap!
            return True
        except ApiException as e:
            print(f"Error: {e}!")

    @property
    def strategy(self):
        return self.cfg['strategy']

    @property
    def target_asset(self):
        return self.strategy['target_asset']

    async def run_loop(self):
        await self.print_balances()
        print(f"Going to buy {self.buy_amount} {self.target_asset}")

        if self.strategy.get('skip_check'):
            print(f"Skipping check")
        else:
            check_interval = self.strategy['check_interval']
            tick = 0
            while True:
                tick += 1
                print(f"#{tick:05} Checking if buy is possible...")
                if await self.check_possibility():
                    print("Buy is possible!!!")
                    break

                await asyncio.sleep(check_interval)

        await self.submit_buy_order()
        print("Done!")

        await asyncio.sleep(1)

    @property
    def buy_amount(self):
        from_asset = self.strategy['source_asset']
        from_amount = self.strategy['source_amount']
        return CryptoAmount.automatic(from_amount, from_asset)

    async def submit_buy_order(self):
        cfg, amm = self.cfg, self.amm
        tx_hash = await amm.swap(self.buy_amount, self.target_asset)
        print(f"Transaction hash: {amm.get_track_url(tx_hash)}")


if __name__ == "__main__":
    asyncio.run(TCYBot.create())
