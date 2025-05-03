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
        phrase = self.cfg['thor']['phrase']
        thornode = self.cfg['thor']['node_url']
        network = self.cfg['thor']['network_id']
        self.query = THORChainQuery.from_thornode_and_midgard(thornode_url=thornode)

        self.client = THORChainClient(
            phrase=phrase,
            client_urls={
                NetworkType(network): NodeURL(thornode)
            }
        )
        self.wallet = Wallet.from_clients([self.client])
        self.amm = THORChainAMM(self.wallet)

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
                self.to_asset,
            )
            print(r)
            if r.can_swap:
                return True
        except ApiException as e:
            print(f"Error: {e}!")

        return False

    async def run_loop(self):
        await self.print_balances()
        check_interval = self.cfg['buy']['check_interval']
        tick = 1
        while True:
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
        from_asset = self.cfg['buy']['asset']
        from_amount = self.cfg['buy']['amount']
        return CryptoAmount.automatic(from_amount, from_asset)

    @property
    def to_asset(self):
        to_asset = "THOR.TCY"
        return to_asset

    async def submit_buy_order(self):
        cfg, amm = self.cfg, self.amm
        tx_hash = await amm.do_swap(self.buy_amount, self.to_asset)
        print(f"Transaction hash: {amm.get_track_url(tx_hash)}")


if __name__ == "__main__":
    asyncio.run(TCYBot.create())
