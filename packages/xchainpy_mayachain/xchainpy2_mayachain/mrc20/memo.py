from xchainpy2_utils import Amount, Asset


def check_ticker(ticker):
    if isinstance(ticker, Asset):
        ticker = ticker.ticker

    if not (1 <= len(ticker) <= 4):
        raise ValueError('Ticker must be 1-4 characters long')

    if not ticker.isalnum():
        raise ValueError('Symbol must contain only letters and digits')

    return ticker


MRC20_DECIMALS = 10


def get_amount(amount, zero_allowed=False):
    amount = Amount.automatic(amount, MRC20_DECIMALS)
    if not zero_allowed and amount.internal_amount <= 0:
        raise ValueError('Must be positive')
    return str(amount.internal_amount)


class MRC20Memo:
    @classmethod
    def deploy_token(cls, ticker, supply, mint_limit=None, mint_price=None) -> str:
        # "MRC-20:deploy:[ticker]:[supply]:[mint-limit]:[mint-price]"
        ticker = check_ticker(ticker)

        supply = get_amount(supply)

        components = ['MRC-20', 'deploy', ticker, supply]
        if mint_limit is not None:
            mint_limit = get_amount(mint_price)
            components.append(mint_limit)
        if mint_price is not None:
            mint_price = get_amount(mint_price)
            components.append(mint_price)
        return ':'.join(components)

    @classmethod
    def set_mint_price(cls, ticker, mint_price) -> str:
        # "MRC-20:set-mint-price:[ticker]:[mint-price]"
        ticker = check_ticker(ticker)
        mint_price = get_amount(mint_price)
        return ':'.join(['MRC-20', 'set-mint-price', ticker, mint_price])

    @classmethod
    def mint(cls, ticker, amount, recipient=None) -> str:
        # "MRC-20:mint:[ticker]:[amount]:[recipient]"
        ticker = check_ticker(ticker)
        amount = get_amount(amount)

        components = ['MRC-20', 'mint', ticker, amount]
        if recipient is not None:
            components.append(recipient)
        return ':'.join(components)

    @classmethod
    def transfer(cls, ticker, amount) -> str:
        # "MRC-20:transfer:[ticker]:[amount]
        ticker = check_ticker(ticker)
        amount = get_amount(amount)

        return ':'.join(['MRC-20', 'transfer', ticker, amount])

    @classmethod
    def sell(cls, ticker, amount, price) -> str:
        # "MRC-20:sell:[ticker]:[amount]:[price]"
        ticker = check_ticker(ticker)
        amount = get_amount(amount)
        price = get_amount(price)

        return ':'.join(['MRC-20', 'sell', ticker, amount, price])

    @classmethod
    def cancel(cls, ticker, tx_hash) -> str:
        # "MRC-20:cancel:[ticker]:[hash]"
        ticker = check_ticker(ticker)
        if not tx_hash:
            raise ValueError('tx_hash must not be empty')
        return ':'.join(['MRC-20', 'cancel', ticker, tx_hash])

    @classmethod
    def buy(cls, ticker, amount, tx_hash) -> str:
        # "MRC-20:buy:[ticker]:[amount]:[hash]"
        ticker = check_ticker(ticker)
        amount = get_amount(amount)

        if not tx_hash:
            raise ValueError('tx_hash must not be empty')

        return ':'.join(['MRC-20', 'buy', ticker, amount, tx_hash])

    @classmethod
    def burn(cls, ticker, amount) -> str:
        # "MRC-20:burn:[ticker]:[amount]"
        ticker = check_ticker(ticker)
        amount = get_amount(amount)

        return ':'.join(['MRC-20', 'burn', ticker, amount])

    @classmethod
    def stake(cls, ticker, amount) -> str:
        # "STAKING:stake:GLD:12340000000000"
        ticker = check_ticker(ticker)
        amount = get_amount(amount)
        return ':'.join(['STAKING', 'stake', ticker, amount])

    @classmethod
    def withdraw_stake(cls, ticker) -> str:
        # "STAKING:withdraw:GLD
        ticker = check_ticker(ticker)
        return ':'.join(['STAKING', 'withdraw', ticker])

    @classmethod
    def claim(cls, ticker) -> str:
        # "STAKING:claim:GLD"
        ticker = check_ticker(ticker)
        return ':'.join(['STAKING', 'claim', ticker])


class MNFTMemo:

    @staticmethod
    def yes_no(value):
        return 'YES' if value else 'NO'

    @classmethod
    def deploy_token(cls, name, symbol, supply, base_url, pre_minted,
                     minted_by_owner_only=None, mint_price=None) -> str:
        # "M-NFT:deploy:[name]:[symbol]:[supply]:[baseURL]:[preMinted]:[mintedByOwnerOnly]:[mintPrice]"

        symbol = check_ticker(symbol)

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
        symbol = check_ticker(symbol)
        mint_price = get_amount(mint_price)
        return ':'.join(['M-NFT', 'update-mint-price', symbol, mint_price])

    @classmethod
    def set_base_url(cls, symbol, base_url) -> str:
        # "M-NFT:set-base-url:[symbol]:[baseURL]"
        symbol = check_ticker(symbol)
        return ':'.join(['M-NFT', 'set-base-url', symbol, base_url])

    @classmethod
    def mint(cls, symbol, token_id=None) -> str:
        # "M-NFT:mint:[symbol]:[id]"
        symbol = check_ticker(symbol)
        components = ['M-NFT', 'mint', symbol]
        if token_id is not None:
            components.append(token_id)
        return ':'.join(components)

    @classmethod
    def transfer(cls, symbol, token_id) -> str:
        # "M-NFT:transfer:[symbol]:[id]"
        symbol = check_ticker(symbol)
        return ':'.join(['M-NFT', 'transfer', symbol, token_id])

    @classmethod
    def sell(cls, symbol, token_id, price) -> str:
        # "M-NFT:sell:[symbol]:[id]:[price]"
        symbol = check_ticker(symbol)
        price = get_amount(price)
        return ':'.join(['M-NFT', 'sell', symbol, token_id, price])

    @classmethod
    def cancel(cls, symbol, token_id) -> str:
        # "M-NFT:cancel:[symbol]:[id]"
        symbol = check_ticker(symbol)
        return ':'.join(['M-NFT', 'cancel', symbol, token_id])

    @classmethod
    def buy(cls, symbol, token_id) -> str:
        # "M-NFT:buy:[symbol]:[id]"
        symbol = check_ticker(symbol)
        return ':'.join(['M-NFT', 'buy', symbol, token_id])
