from typing import Union

from .const import MRC20_DECIMALS
from xchainpy2_utils import Amount, Asset


def check_ticker(ticker: Union[Asset, str]):
    """
    Check if the MRC20 ticker is valid.

    :param ticker: Asset or str
    :return: bool
    """
    if isinstance(ticker, Asset):
        ticker = ticker.ticker

    if not (1 <= len(ticker) <= 4):
        raise ValueError('Ticker must be 1-4 characters long')

    if not ticker.isalnum():
        raise ValueError('Symbol must contain only letters and digits')

    return ticker


def get_amount(amount, zero_allowed=False):
    """
    Helper function to convert an amount to a string suitable for a memo.

    :param amount: Amount or str
    :param zero_allowed: if zero amounts are allowed
    """

    amount = Amount.automatic(amount, MRC20_DECIMALS)
    if not zero_allowed and amount.internal_amount <= 0:
        raise ValueError('Must be positive')
    return str(amount.internal_amount)


class MRC20Memo:
    """
    MRC20Memo is a class that provides methods to generate memos for MRC20 transactions.
    """

    @classmethod
    def deploy_token(cls, ticker, supply, mint_limit=None, mint_price=None) -> str:
        """
        Generate a memo for deploying a MRC20 token.

        :param ticker: The ticker of a new token
        :param supply: Total supply of the token. See: Amount.automatic
        :param mint_limit: The maximum amount of tokens that can be minted. See: Amount.automatic
        :param mint_price: The price of minting a token in Cacao. See: Amount.automatic
        :return: Memo string
        """

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
        """
        Generate a memo for setting the mint price of a MRC20 token.

        :param ticker: MRC20 token ticker
        :param mint_price: The price of minting a token in Cacao. See: AmountInitTypes
        :return: Memo string
        """

        # "MRC-20:set-mint-price:[ticker]:[mint-price]"
        ticker = check_ticker(ticker)
        mint_price = get_amount(mint_price)
        return ':'.join(['MRC-20', 'set-mint-price', ticker, mint_price])

    @classmethod
    def mint(cls, ticker, amount, recipient=None) -> str:
        """
        Generate a memo for minting a MRC20 token.

        :param ticker: MRC20 token ticker
        :param amount: Amount to mint
        :param recipient: Recipient of the minted tokens
        :return: Memo string
        """

        # "MRC-20:mint:[ticker]:[amount]:[recipient]"
        ticker = check_ticker(ticker)
        amount = get_amount(amount)

        components = ['MRC-20', 'mint', ticker, amount]
        if recipient is not None:
            components.append(recipient)
        return ':'.join(components)

    @classmethod
    def transfer(cls, ticker, amount) -> str:
        """
        Generate a memo for transferring a MRC20 token.

        :param ticker: MRC20 token ticker
        :param amount: Amount to transfer
        :return: Memo string
        """
        # "MRC-20:transfer:[ticker]:[amount]
        ticker = check_ticker(ticker)
        amount = get_amount(amount)

        return ':'.join(['MRC-20', 'transfer', ticker, amount])

    @classmethod
    def sell(cls, ticker, amount, price) -> str:
        """
        Generate a memo for placing a sell order for a MRC20 token.

        :param ticker: MRC20 token ticker
        :param amount: Amount to sell
        :param price: Price per token in Cacao. See: AmountInitTypes
        :return: Memo string
        """
        # "MRC-20:sell:[ticker]:[amount]:[price]"
        ticker = check_ticker(ticker)
        amount = get_amount(amount)
        price = get_amount(price)

        return ':'.join(['MRC-20', 'sell', ticker, amount, price])

    @classmethod
    def cancel(cls, ticker, tx_hash) -> str:
        """
        Generate a memo for cancelling a MRC20 token sell order.

        :param ticker: MRC20 token ticker
        :param tx_hash: Transaction hash of the order to cancel
        :return: Memo string
        """
        # "MRC-20:cancel:[ticker]:[hash]"
        ticker = check_ticker(ticker)
        if not tx_hash:
            raise ValueError('tx_hash must not be empty')
        return ':'.join(['MRC-20', 'cancel', ticker, tx_hash])

    @classmethod
    def buy(cls, ticker, amount, tx_hash) -> str:
        """
        Generate a memo for fulfilling a buy order for a MRC20 token.

        :param ticker: MRC20 token ticker
        :param amount: Amount to buy
        :param tx_hash: Transaction hash of the order to fulfill
        :return: Memo string
        """
        # "MRC-20:buy:[ticker]:[amount]:[hash]"
        ticker = check_ticker(ticker)
        amount = get_amount(amount)

        if not tx_hash:
            raise ValueError('tx_hash must not be empty')

        return ':'.join(['MRC-20', 'buy', ticker, amount, tx_hash])

    @classmethod
    def burn(cls, ticker, amount) -> str:
        """
        Generate a memo for burning a MRC20 token.

        :param ticker: MRC20 token ticker
        :param amount: Amount to burn
        :return: Memo string
        """
        # "MRC-20:burn:[ticker]:[amount]"
        ticker = check_ticker(ticker)
        amount = get_amount(amount)

        return ':'.join(['MRC-20', 'burn', ticker, amount])

    @classmethod
    def stake(cls, ticker, amount) -> str:
        """
        Generate a memo for staking a MRC20 token.

        :param ticker: MRC20 token ticker
        :param amount: Amount to stake
        :return: Memo string
        """
        # "STAKING:stake:GLD:12340000000000"
        ticker = check_ticker(ticker)
        amount = get_amount(amount)
        return ':'.join(['STAKING', 'stake', ticker, amount])

    @classmethod
    def withdraw_stake(cls, ticker) -> str:
        """
        Generate a memo for withdrawing a staked MRC20 token.

        :param ticker: MRC20 token ticker
        :return: Memo string
        """
        # "STAKING:withdraw:GLD
        ticker = check_ticker(ticker)
        return ':'.join(['STAKING', 'withdraw', ticker])

    @classmethod
    def claim(cls, ticker) -> str:
        """
        Generate a memo for claiming staking rewards.

        :param ticker: MRC20 token ticker
        :return: Memo string
        """
        # "STAKING:claim:GLD"
        ticker = check_ticker(ticker)
        return ':'.join(['STAKING', 'claim', ticker])


class MNFTMemo:
    """
    MNFTMemo is a class that provides methods to generate memos for M-NFT transactions.
    """

    @staticmethod
    def yes_no(value) -> str:
        """
        Convert a boolean value to YES or NO string

        :param value: any boolean-like value
        :return: str
        """
        return 'YES' if value else 'NO'

    @classmethod
    def deploy_token(cls, name, symbol, supply, base_url, pre_minted,
                     minted_by_owner_only=None, mint_price=None) -> str:
        """
        Generate a memo for deploying a new M-NFT token.
        https://docs.mayaprotocol.com/blockchain-explorer/mayascan/m-nfts

        :param name: Name of the token 1-20 characters long
        :param symbol: Symbol of the token
        :param supply: Supply of the token 1-100000
        :param base_url: Base URL for the token metadata
        :param pre_minted: Whether the token is pre-minted
        :param minted_by_owner_only: Whether the token can only be minted by the owner
        :param mint_price: Price of minting a token in Cacao
        :return: Memo string
        """

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
        """
        Generate a memo for updating the mint price of a M-NFT token.

        :param symbol: M-NFT token symbol
        :param mint_price: Mint price in Cacao
        :return: Memo string
        """
        # "M-NFT:update-mint-price:[symbol]:[mintPrice]"
        symbol = check_ticker(symbol)
        mint_price = get_amount(mint_price)
        return ':'.join(['M-NFT', 'update-mint-price', symbol, mint_price])

    @classmethod
    def set_base_url(cls, symbol, base_url) -> str:
        """
        Generate a memo for setting the base URL of a M-NFT token.

        :param symbol: M-NFT token symbol
        :param base_url: Base URL for the token metadata
        :return: Memo string
        """
        # "M-NFT:set-base-url:[symbol]:[baseURL]"
        symbol = check_ticker(symbol)
        return ':'.join(['M-NFT', 'set-base-url', symbol, base_url])

    @classmethod
    def mint(cls, symbol, token_id=None) -> str:
        """
        Generate a memo for minting a M-NFT token.

        :param symbol: M-NFT token symbol
        :param token_id: Token identifier to mint
        :return: Memo string
        """
        # "M-NFT:mint:[symbol]:[id]"
        symbol = check_ticker(symbol)
        components = ['M-NFT', 'mint', symbol]
        if token_id is not None:
            components.append(token_id)
        return ':'.join(components)

    @classmethod
    def transfer(cls, symbol, token_id) -> str:
        """
        Generate a memo for transferring M-NFT token.
        The token is transferred to the recipient address of the transaction.

        :param symbol: M-NFT token symbol
        :param token_id: Token identifier to transfer
        :return: Memo string
        """

        # "M-NFT:transfer:[symbol]:[id]"
        symbol = check_ticker(symbol)
        return ':'.join(['M-NFT', 'transfer', symbol, token_id])

    @classmethod
    def sell(cls, symbol, token_id, price) -> str:
        """
        Generate a memo for placing a sell order for a M-NFT token.

        :param symbol: M-NFT token symbol
        :param token_id: Token identifier to sell
        :param price: Sale price in Cacao
        :return: Memo string
        """

        # "M-NFT:sell:[symbol]:[id]:[price]"
        symbol = check_ticker(symbol)
        price = get_amount(price)
        return ':'.join(['M-NFT', 'sell', symbol, token_id, price])

    @classmethod
    def cancel(cls, symbol, token_id) -> str:
        """
        Generate a memo for cancelling a sell order for a M-NFT token.

        :param symbol: M-NFT token symbol
        :param token_id: Token identifier to cancel
        :return: Memo string
        """
        # "M-NFT:cancel:[symbol]:[id]"
        symbol = check_ticker(symbol)
        return ':'.join(['M-NFT', 'cancel', symbol, token_id])

    @classmethod
    def buy(cls, symbol, token_id) -> str:
        """
        Generate a memo for fulfilling an order to buy M-NFT token.

        :param symbol: M-NFT token symbol
        :param token_id: Token identifier to buy
        :return: Memo string
        """
        # "M-NFT:buy:[symbol]:[id]"
        symbol = check_ticker(symbol)
        return ':'.join(['M-NFT', 'buy', symbol, token_id])
