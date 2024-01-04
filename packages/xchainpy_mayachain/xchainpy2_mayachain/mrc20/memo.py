from xchainpy2_utils import Amount


def check_ticker(ticker):
    if not (1 <= len(ticker) <= 4):
        raise ValueError('Ticker must be 1-4 characters long')

    if not ticker.isalnum():
        raise ValueError('Symbol must contain only letters and digits')


MRC20_DECIMALS = 10


def get_amount(amount):
    return Amount.automatic(amount, MRC20_DECIMALS)


class MRC20Memo:
    @classmethod
    def deploy_token(cls, ticker, supply, mint_limit=None, mint_price=None) -> str:
        # "MRC-20:deploy:[ticker]:[supply]:[mint-limit]:[mint-price]"
        check_ticker(ticker)

        supply = get_amount(supply)
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
        check_ticker(ticker)
        mint_price = get_amount(mint_price)
        return ':'.join(['MRC-20', 'set-mint-price', ticker, mint_price])

    @classmethod
    def mint(cls, ticker, amount, recipient=None) -> str:
        # "MRC-20:mint:[ticker]:[amount]:[recipient]"
        check_ticker(ticker)
        amount = get_amount(amount)
        if amount.internal_amount <= 0:
            raise ValueError('Amount must be positive')

        components = ['MRC-20', 'mint', ticker, amount]
        if recipient is not None:
            components.append(recipient)
        return ':'.join(components)

    @classmethod
    def transfer(cls, ticker, amount) -> str:
        # "MRC-20:transfer:[ticker]:[amount]
        check_ticker(ticker)
        amount = get_amount(amount)
        if amount.internal_amount <= 0:
            raise ValueError('Amount must be positive')

        return ':'.join(['MRC-20', 'transfer', ticker, amount])

    @classmethod
    def sell(cls, ticker, amount, price) -> str:
        # "MRC-20:sell:[ticker]:[amount]:[price]"
        check_ticker(ticker)
        amount = get_amount(amount)
        if amount.internal_amount <= 0:
            raise ValueError('Amount must be positive')

        price = get_amount(price)
        if price.internal_amount <= 0:
            raise ValueError('Price must be positive')

        return ':'.join(['MRC-20', 'sell', ticker, amount, price])

    @classmethod
    def cancel(cls, ticker, tx_hash) -> str:
        # "MRC-20:cancel:[ticker]:[hash]"
        check_ticker(ticker)
        if not tx_hash:
            raise ValueError('tx_hash must not be empty')
        return ':'.join(['MRC-20', 'cancel', ticker, tx_hash])

    @classmethod
    def buy(cls, ticker, amount, tx_hash) -> str:
        # "MRC-20:buy:[ticker]:[amount]:[hash]"
        check_ticker(ticker)
        amount = get_amount(amount)
        if amount.internal_amount <= 0:
            raise ValueError('Amount must be positive')

        if not tx_hash:
            raise ValueError('tx_hash must not be empty')

        return ':'.join(['MRC-20', 'buy', ticker, amount, tx_hash])

    @classmethod
    def burn(cls, ticker, amount) -> str:
        # "MRC-20:burn:[ticker]:[amount]"
        check_ticker(ticker)
        amount = get_amount(amount)
        if amount.internal_amount <= 0:
            raise ValueError('Amount must be positive')

        return ':'.join(['MRC-20', 'burn', ticker, amount])


class MNFTMemo:

    @staticmethod
    def yes_no(value):
        return 'YES' if value else 'NO'

    @classmethod
    def deploy_token(cls, name, symbol, supply, base_url, pre_minted,
                     minted_by_owner_only=None, mint_price=None) -> str:
        # "M-NFT:deploy:[name]:[symbol]:[supply]:[baseURL]:[preMinted]:[mintedByOwnerOnly]:[mintPrice]"

        check_ticker(symbol)

        symbol = symbol.upper()

        if not (1 <= len(name) <= 20):
            raise ValueError('Name must be 1-20 characters long')

        supply = int(supply)
        if not (1 <= supply <= 100000):
            raise ValueError('Supply must be between 1 and 100000')

        components = ['M-NFT', 'deploy', name, symbol, supply, base_url, cls.yes_no(pre_minted)]

        if minted_by_owner_only is not None:
            components.append(cls.yes_no(minted_by_owner_only))
        if mint_price is not None:
            components.append(mint_price)

        return ':'.join(components)

    @classmethod
    def update_mint_price(cls, symbol, mint_price) -> str:
        # "M-NFT:update-mint-price:[symbol]:[mintPrice]"
        check_ticker(symbol)
        mint_price = get_amount(mint_price)
        return ':'.join(['M-NFT', 'update-mint-price', symbol, mint_price])

    @classmethod
    def set_base_url(cls, symbol, base_url) -> str:
        # "M-NFT:set-base-url:[symbol]:[baseURL]"
        check_ticker(symbol)
        return ':'.join(['M-NFT', 'set-base-url', symbol, base_url])

    @classmethod
    def mint(cls, symbol, token_id=None) -> str:
        # "M-NFT:mint:[symbol]:[id]"
        check_ticker(symbol)
        components = ['M-NFT', 'mint', symbol]
        if token_id is not None:
            components.append(token_id)
        return ':'.join(components)

    @classmethod
    def transfer(cls, symbol, token_id) -> str:
        # "M-NFT:transfer:[symbol]:[id]"
        check_ticker(symbol)
        return ':'.join(['M-NFT', 'transfer', symbol, token_id])

    @classmethod
    def sell(cls, symbol, token_id, price) -> str:
        # "M-NFT:sell:[symbol]:[id]:[price]"
        check_ticker(symbol)
        price = get_amount(price)
        return ':'.join(['M-NFT', 'sell', symbol, token_id, price])

    @classmethod
    def cancel(cls, symbol, token_id) -> str:
        # "M-NFT:cancel:[symbol]:[id]"
        check_ticker(symbol)
        return ':'.join(['M-NFT', 'cancel', symbol, token_id])

    @classmethod
    def buy(cls, symbol, token_id) -> str:
        # "M-NFT:buy:[symbol]:[id]"
        check_ticker(symbol)
        return ':'.join(['M-NFT', 'buy', symbol, token_id])
