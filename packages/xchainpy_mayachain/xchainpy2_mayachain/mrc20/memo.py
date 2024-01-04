from xchainpy2_utils import Amount


class MRC20Memo:
    DECIMALS = 10

    @staticmethod
    def check_ticker(ticker):
        if not (1 <= len(ticker) <= 4):
            raise ValueError('Ticker must be 1-4 characters long')

    @classmethod
    def get_amount(cls, amount):
        return Amount.automatic(amount, cls.DECIMALS)

    @classmethod
    def deploy_token(cls, ticker, supply, mint_limit=None, mint_price=None) -> str:
        # "MRC-20:deploy:[ticker]:[supply]:[mint-limit]:[mint-price]"
        cls.check_ticker(ticker)

        supply = cls.get_amount(supply)
        if supply.internal_amount <= 0:
            raise ValueError('Supply must be positive')

        components = ['MRC-20', 'deploy', ticker, supply]
        if mint_limit is not None:
            components.append(mint_limit)
        if mint_price is not None:
            components.append(mint_price)
        return ':'.join(components)

    @classmethod
    def set_mint_price(cls, ticker, mint_price) -> str:
        # "MRC-20:set-mint-price:[ticker]:[mint-price]"
        cls.check_ticker(ticker)
        mint_price = cls.get_amount(mint_price)
        return ':'.join(['MRC-20', 'set-mint-price', ticker, mint_price])

    @classmethod
    def mint(cls, ticker, amount, recipient=None) -> str:
        # "MRC-20:mint:[ticker]:[amount]:[recipient]"
        cls.check_ticker(ticker)
        amount = cls.get_amount(amount)
        if amount.internal_amount <= 0:
            raise ValueError('Amount must be positive')

        components = ['MRC-20', 'mint', ticker, amount]
        if recipient is not None:
            components.append(recipient)
        return ':'.join(components)

    @classmethod
    def transfer(cls, ticker, amount) -> str:
        # "MRC-20:transfer:[ticker]:[amount]
        cls.check_ticker(ticker)
        amount = cls.get_amount(amount)
        if amount.internal_amount <= 0:
            raise ValueError('Amount must be positive')

        return ':'.join(['MRC-20', 'transfer', ticker, amount])

    @classmethod
    def sell(cls, ticker, amount, price) -> str:
        # "MRC-20:sell:[ticker]:[amount]:[price]"
        cls.check_ticker(ticker)
        amount = cls.get_amount(amount)
        if amount.internal_amount <= 0:
            raise ValueError('Amount must be positive')

        price = cls.get_amount(price)
        if price.internal_amount <= 0:
            raise ValueError('Price must be positive')

        return ':'.join(['MRC-20', 'sell', ticker, amount, price])

    @classmethod
    def cancel(cls, ticker, tx_hash) -> str:
        # "MRC-20:cancel:[ticker]:[hash]"
        cls.check_ticker(ticker)
        if not tx_hash:
            raise ValueError('tx_hash must not be empty')
        return ':'.join(['MRC-20', 'cancel', ticker, tx_hash])

    @classmethod
    def buy(cls, ticker, amount, tx_hash) -> str:
        # "MRC-20:buy:[ticker]:[amount]:[hash]"
        cls.check_ticker(ticker)
        amount = cls.get_amount(amount)
        if amount.internal_amount <= 0:
            raise ValueError('Amount must be positive')

        if not tx_hash:
            raise ValueError('tx_hash must not be empty')

        return ':'.join(['MRC-20', 'buy', ticker, amount, tx_hash])

    @classmethod
    def burn(cls, ticker, amount) -> str:
        # "MRC-20:burn:[ticker]:[amount]"
        cls.check_ticker(ticker)
        amount = cls.get_amount(amount)
        if amount.internal_amount <= 0:
            raise ValueError('Amount must be positive')

        return ':'.join(['MRC-20', 'burn', ticker, amount])
