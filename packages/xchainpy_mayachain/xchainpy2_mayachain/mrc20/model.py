from typing import NamedTuple


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
