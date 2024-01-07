from typing import NamedTuple, List


class MRC20Token(NamedTuple):
    ticker: str
    hash: str
    height: int
    supply: int
    minted: int
    burnt: int
    owner: str
    memo: str
    date: str
    listed: bool
    max_mint_per_address: int
    mint_price_per_token: int
    name: str
    description: str
    logo: str
    volume_transfer: int
    volume_mint: int
    volume_buy: int
    volume_sell: int
    volume_transfer_cacao: int
    volume_mint_cacao: int
    volume_buy_cacao: int
    volume_sell_cacao: int
    holders: int
    holders_balance: int

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
    def from_api(cls, resp):
        return [cls.from_dict(d) for d in resp['tokens']]


class MNFTToken(NamedTuple):
    symbol: str
    hash: str
    height: int
    name: str
    supply: int
    base_url: str
    pre_minted: bool
    minted_by_owner_only: bool
    mint_price: int
    owner: str
    date: str
    listed: bool
    minted: int
    listed_for_sale: int
    floor_price: int
    volume_transfer: int
    volume_mint: int
    volume_buy: int
    volume_sell: int
    volume_transfer_cacao: int
    volume_mint_cacao: int
    volume_buy_cacao: int
    volume_sell_cacao: int
    holders: int
    holders_balance: int

    @classmethod
    def from_dict(cls, d):
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
    def from_api(cls, resp):
        return [cls.from_dict(d) for d in resp['collections']]


class MRC20Price(NamedTuple):
    ticker: str
    price_in_cacao: float
    price_in_usd: float
    decimals: int

    @classmethod
    def from_dict(cls, d):
        return cls(
            ticker=d['ticker'],
            price_in_cacao=float(d['priceInCacao']),
            price_in_usd=float(d['priceInUsd']),
            decimals=d['decimals'],
        )


class MRC20Order(NamedTuple):
    hash: str
    ticker: str
    address: str
    balance: int
    price: int
    height: int
    date: str
    sellers_balance_remaining: int

    @classmethod
    def from_dict(cls, d):
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
    def from_api(cls, resp):
        return [cls.from_dict(d) for d in resp]


class MNFTOrder(NamedTuple):
    hash: str
    symbol: str
    address: str
    id: int
    price: int
    height: int
    date: str

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
    symbol: str
    ids: List[int]
    name: str
    base_url: str

    @classmethod
    def from_dict(cls, d):
        return cls(
            symbol=d['symbol'],
            ids=d['ids'],
            name=d['name'],
            base_url=d['base_url'],
        )


class SendAction(NamedTuple):
    hash: str
    height: int
    from_: str
    to: str
    asset: str
    amount: str
    memo: str
    date: str

    @classmethod
    def from_dict(cls, d):
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
    total: int
    actions: List[SendAction]

    @classmethod
    def from_response(cls, d):
        return cls(
            total=d['total'],
            actions=[SendAction.from_dict(action) for action in d['list']],
        )


class MRC20StakingInfo(NamedTuple):
    ticker: str
    pool: int
    apr: int
    stakers: int
    staked: int
    claimed: int

    @classmethod
    def from_dict(cls, d):
        return cls(
            ticker=d['ticker'],
            pool=int(d['pool']),
            apr=d['apr'],
            stakers=int(d['stakers']),
            staked=int(d['staked']),
            claimed=d['claimed'],
        )


class MRC20StakingBalance(NamedTuple):
    added: int
    claimed: int
    claimable: float

    @classmethod
    def from_dict(cls, d):
        return cls(
            added=int(d['added']),
            claimed=int(d['claimed']),
            claimable=float(d['claimable']),
        )


class MRC20Balance(NamedTuple):
    ticker: str
    balance: int
    balance_for_sale: int
    balance_staked: int
    name: str
    logo: str
    logo_full_path: str
    price_in_cacao: float
    price_in_usd: float
    decimals: int

    @classmethod
    def from_dict(cls, d):
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