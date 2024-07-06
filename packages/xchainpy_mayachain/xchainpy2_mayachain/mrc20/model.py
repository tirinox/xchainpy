from typing import NamedTuple, List


class MRC20Token(NamedTuple):
    """
    This class represents a MRC20 token description.
    """

    ticker: str
    """Token ticker"""

    hash: str
    """Token hash. Not sure what this is for"""

    height: int
    """Block height, where the token was created"""

    supply: int
    """Total supply of the token"""

    minted: int
    """Total amount of the token that has been minted so far"""

    burnt: int
    """Total amount of the token that has been burnt so far"""

    owner: str
    """Maya address of the token owner"""

    memo: str
    """Memo of the token. Not sure what this is for"""

    date: str
    """Date when the token was created"""

    listed: bool
    """Whether the token is listed or not"""

    max_mint_per_address: int
    """Maximum amount of the token that can be minted per address"""

    mint_price_per_token: int
    """Price of minting the token per token"""

    name: str
    """Name of the token"""

    description: str
    """Description of the token"""

    logo: str
    """URL of the token logo"""

    volume_transfer: int
    """Volume of the token transferred"""

    volume_mint: int
    """Volume of the token minted"""

    volume_buy: int
    """Volume of the token bought"""

    volume_sell: int
    """Volume of the token sold"""

    volume_transfer_cacao: int
    """Volume of the token transferred in Cacao"""

    volume_mint_cacao: int
    """Volume of the token minted in Cacao"""

    volume_buy_cacao: int
    """Volume of the token bought in Cacao"""

    volume_sell_cacao: int
    """Volume of the token sold in Cacao"""

    holders: int
    """Number of token holders"""

    holders_balance: int
    """Total balance of the token holders"""

    @classmethod
    def from_dict(cls, d):
        return cls(
            ticker=d['ticker'],
            hash=d['hash'],
            height=d['height'],
            supply=d['supply'],
            minted=d['minted'],
            burnt=d['burnt'],
            owner=d['owner'],
            memo=d['memo'],
            date=d['date'],
            listed=d['listed'],
            max_mint_per_address=d['max_mint_per_address'],
            mint_price_per_token=d['mint_price_per_token'],
            name=d['name'],
            description=d['description'],
            logo=d['logo'],
            volume_transfer=d['volume_transfer'],
            volume_mint=d['volume_mint'],
            volume_buy=d['volume_buy'],
            volume_sell=d['volume_sell'],
            volume_transfer_cacao=d['volume_transfer_cacao'],
            volume_mint_cacao=d['volume_mint_cacao'],
            volume_buy_cacao=d['volume_buy_cacao'],
            volume_sell_cacao=d['volume_sell_cacao'],
            holders=d['holders'],
            holders_balance=d['holders_balance'],
        )

    @classmethod
    def from_api(cls, resp) -> List['MRC20Token']:
        """
        Create a list of MRC20Token objects from an API response.

        :param resp: Response from the Maya API
        :return: List of MRC20Token objects
        """
        return [cls.from_dict(d) for d in resp['tokens']]


class MNFTToken(NamedTuple):
    """
    M-NFT token description
    """

    symbol: str
    """Symbol of the token"""

    hash: str
    """Hash of the token"""

    height: int
    """Block height where the token was created"""

    name: str
    """Name of the token"""

    supply: int
    """Total supply of the token"""

    base_url: str
    """Base URL of the token metadata"""

    pre_minted: bool
    """Whether the token is pre-minted or not"""

    minted_by_owner_only: bool
    """Whether the token can be minted by the owner only"""

    mint_price: int
    """Price of minting the token"""

    owner: str
    """Address of the token owner"""

    date: str
    """Date when the token was created"""

    listed: bool
    """Whether the token is listed or not"""

    minted: int
    """Total amount of the token that has been minted so far"""

    listed_for_sale: int
    """Total amount of the token that has been listed for sale"""

    floor_price: int
    """Floor price of the token"""

    volume_transfer: int
    """Volume of the token transferred"""

    volume_mint: int
    """Volume of the token minted"""

    volume_buy: int
    """Volume of the token bought"""

    volume_sell: int
    """Volume of the token sold"""

    volume_transfer_cacao: int
    """Volume of the token transferred in Cacao"""

    volume_mint_cacao: int
    """Volume of the token minted in Cacao"""

    volume_buy_cacao: int
    """Volume of the token bought in Cacao"""

    volume_sell_cacao: int
    """Volume of the token sold in Cacao"""

    holders: int
    """Number of token holders"""

    holders_balance: int
    """Total balance of the token holders"""

    @classmethod
    def from_dict(cls, d) -> 'MNFTToken':
        """
        Create a MNFTToken object from a dictionary.

        :param d: Input dictionary
        :return: MNFTToken object
        """
        return cls(
            symbol=d['symbol'],
            hash=d['hash'],
            height=d['height'],
            name=d['name'],
            supply=d['supply'],
            base_url=d['base_url'],
            pre_minted=d['pre_minted'],
            minted_by_owner_only=d['minted_by_owner_only'],
            mint_price=d['mint_price'],
            owner=d['owner'],
            date=d['date'],
            listed=d['listed'],
            minted=d['minted'],
            listed_for_sale=d['listed_for_sale'],
            floor_price=d['floor_price'],
            volume_transfer=d['volume_transfer'],
            volume_mint=d['volume_mint'],
            volume_buy=d['volume_buy'],
            volume_sell=d['volume_sell'],
            volume_transfer_cacao=d['volume_transfer_cacao'],
            volume_mint_cacao=d['volume_mint_cacao'],
            volume_buy_cacao=d['volume_buy_cacao'],
            volume_sell_cacao=d['volume_sell_cacao'],
            holders=d['holders'],
            holders_balance=d['holders_balance'],
        )

    @classmethod
    def from_api(cls, resp) -> List['MNFTToken']:
        """
        Create a list of MNFTToken objects from an API response.

        :param resp: Response from the Maya API
        :return: List of MNFTToken objects
        :rtype: List[MNFTToken]
        """
        return [cls.from_dict(d) for d in resp['collections']]


class MRC20Price(NamedTuple):
    """
    This class represents the price of a MRC20 token.
    """

    ticker: str
    """MRC20 token ticker"""

    price_in_cacao: float
    """Price of the token in Cacao"""

    price_in_usd: float
    """Price of the token in USD"""

    decimals: int
    """Number of decimals places for the token"""

    @classmethod
    def from_dict(cls, d) -> 'MRC20Price':
        """
        Create a MRC20Price object from a dictionary.

        :param d: Input dictionary
        :return: MRC20Price object
        """
        return cls(
            ticker=d['ticker'],
            price_in_cacao=float(d['priceInCacao']),
            price_in_usd=float(d['priceInUsd']),
            decimals=d['decimals'],
        )


class MRC20Order(NamedTuple):
    """
    This class represents a sell order of a MRC20 token.
    """

    hash: str
    """Hash of the sell order transaction"""

    ticker: str
    """Symbol of the MRC20 token"""

    address: str
    """Seller address"""

    balance: int
    """Balance of the token"""

    price: int
    """Price of the token in Cacao"""

    height: int
    """Block height of the sell order transaction"""

    date: str
    """Date string of the sell order transaction"""

    sellers_balance_remaining: int
    """Remaining balance of the order"""

    @classmethod
    def from_dict(cls, d) -> 'MRC20Order':
        """
        Create a MRC20Order object from a dictionary.

        :param d: Input dictionary
        :return: MRC20Order object
        """
        return cls(
            hash=d['hash'],
            ticker=d['ticker'],
            address=d['address'],
            balance=d['balance'],
            price=d['price'],
            height=d['height'],
            date=d['date'],
            sellers_balance_remaining=d['sellers_balance_remaining'],
        )

    @classmethod
    def from_api(cls, resp) -> List['MRC20Order']:
        """
        Create a list of MRC20Order objects from an API response.

        :param resp: Maya API response
        :return: List of MRC20Order objects
        :rtype: List[MRC20Order]
        """
        return [cls.from_dict(d) for d in resp]


class MNFTOrder(NamedTuple):
    """
    This class represents a sell order of a M-NFT token.
    """

    hash: str
    """Hash of the sell order transaction"""

    symbol: str
    """Symbol of the token"""

    address: str
    """Seller address"""

    id: int
    """Token ID"""

    price: int
    """Price of the token in Cacao"""

    height: int
    """Block height of the sell order transaction"""

    date: str
    """Date string of the sell order transaction"""

    @classmethod
    def from_dict(cls, d):
        return cls(
            hash=d['hash'],
            symbol=d['symbol'],
            address=d['address'],
            id=d['id'],
            price=d['price'],
            height=d['height'],
            date=d['date'],
        )

    @classmethod
    def from_api(cls, resp):
        return [cls.from_dict(d) for d in resp]


class MNFTBalance(NamedTuple):
    """
    This class represents the balance of M-NFT tokens of an address.
    """

    symbol: str
    """Symbol of the token"""

    ids: List[int]
    """List of token IDs"""

    name: str
    """Name of the token"""

    base_url: str
    """Base URL of the token metadata"""

    @classmethod
    def from_dict(cls, d) -> 'MNFTBalance':
        """
        Create a MNFTBalance object from a dictionary.

        :param d: Input dictionary
        :return: MNFTBalance object
        """
        return cls(
            symbol=d['symbol'],
            ids=d['ids'],
            name=d['name'],
            base_url=d['base_url'],
        )


class SendAction(NamedTuple):
    """
    This class represents a send action of MRC20 tokens.
    """

    hash: str
    """Hash of the send action transaction"""

    height: int
    """Block height of the send action transaction"""

    from_: str
    """Sender address"""

    to: str
    """Receiver address"""

    asset: str
    """Asset ticker"""

    amount: str
    """Amount of the asset that was sent"""

    memo: str
    """Memo of the send action transaction"""

    date: str
    """Date string of the send action transaction"""

    @classmethod
    def from_dict(cls, d) -> 'SendAction':
        """
        Create a SendAction object from a dictionary.

        :param d: Input dictionary
        :return: SendAction object
        """
        return cls(
            hash=d['hash'],
            height=d['height'],
            from_=d['from'],
            to=d['to'],
            asset=d['asset'],
            amount=d['amount'],
            memo=d['memo'],
            date=d['date'],
        )


class SendActionResponse(NamedTuple):
    """
    This class represents the response of a send action of MRC20 tokens.
    """

    total: int
    """Total number of send actions in the response"""

    actions: List[SendAction]
    """List of send actions in the response"""

    @classmethod
    def from_response(cls, d) -> 'SendActionResponse':
        """
        Create a SendActionResponse object from a response dictionary.

        :param d: Input dictionary
        :return: SendActionResponse object
        """
        return cls(
            total=d['total'],
            actions=[SendAction.from_dict(action) for action in d['list']],
        )


class MRC20StakingInfo(NamedTuple):
    """
    This class represents the staking information of a MRC20 token.
    """

    ticker: str
    """MRC20 token ticker"""

    pool: int
    """Amount of the token in the staking pool"""

    apr: float
    """Annual Percentage Rate of the token staking pool"""

    stakers: int
    """Number of stakers in the staking pool"""

    staked: int
    """Amount of the token staked in the staking pool"""

    claimed: int
    """Amount of the staking rewards that has been claimed from the staking pool"""

    @classmethod
    def from_dict(cls, d) -> 'MRC20StakingInfo':
        """
        Create a MRC20StakingInfo object from a dictionary.

        :param d: Input dictionary
        :return: MRC20StakingInfo object
        """
        return cls(
            ticker=d['ticker'],
            pool=int(d['pool']),
            apr=d['apr'],
            stakers=int(d['stakers']),
            staked=int(d['staked']),
            claimed=d['claimed'],
        )


class MRC20StakingBalance(NamedTuple):
    """
    This class represents the staking balance of a MRC20 token.
    """

    added: int
    """Amount of the token that was added to the staking pool"""

    claimed: int
    """Amount of the token that has been claimed so far"""

    claimable: float
    """Amount of the token that can be claimed"""

    @classmethod
    def from_dict(cls, d) -> 'MRC20StakingBalance':
        """
        Create a MRC20StakingBalance object from a dictionary.

        :param d: Input dictionary
        :return: MRC20StakingBalance object
        """
        return cls(
            added=int(d['added']),
            claimed=int(d['claimed']),
            claimable=float(d['claimable']),
        )


class MRC20Balance(NamedTuple):
    """
    This class represents the balance of a MRC20 token
    """

    ticker: str
    """MRC20 token ticker"""

    balance: int
    """Balance of the token"""
    balance_for_sale: int
    """Balance of the token that is available for sale"""

    balance_staked: int
    """Balance of the token that is staked"""

    name: str
    """Name of the token"""

    logo: str
    """URL of the token logo"""

    logo_full_path: str
    """Full path of the token logo"""

    price_in_cacao: float
    """Price of the token in Cacao"""

    price_in_usd: float
    """Price of the token in USD"""

    decimals: int
    """Number of decimals places for the token"""

    @classmethod
    def from_dict(cls, d) -> 'MRC20Balance':
        """
        Create a MRC20Balance object from a dictionary.

        :param d: Input dictionary
        :return: MRC20Balance object
        """
        for_sale = int(d.get('balance_for_sale', 0) or 0)
        staked = int(d.get('balance_staked', 0) or 0)
        return cls(
            ticker=d['ticker'],
            balance=int(d['balance']),
            balance_for_sale=for_sale,
            balance_staked=staked,
            name=d['name'],
            logo=d['logo'],
            logo_full_path=d['logoFullPath'],
            price_in_cacao=float(d['priceInCacao']),
            price_in_usd=float(d['priceInUsd']),
            decimals=int(d['decimals']),
        )