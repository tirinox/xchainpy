from xchainpy2_thorchain_query import THORChainQuery


class THORChainAMM:
    def __init__(self, query: THORChainQuery):
        self.query = query

    async def do_swap(self):
        ...

    async def add_liquidity(self):
        ...

    async def remove_liquidity(self):
        ...

    async def borrow(self):
        ...

    async def repay_loan(self):
        ...

    async def add_savers(self):
        ...

    async def remove_savers(self):
        ...

    async def register_name(self):
        ...
