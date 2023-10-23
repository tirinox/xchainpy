from dataclasses import dataclass
from typing import Union

from .consts import ActionType
from .utils import bp_to_float

MEMO_ACTION_TABLE = {
    "add": ActionType.ADD_LIQUIDITY,
    "+": ActionType.ADD_LIQUIDITY,
    "withdraw": ActionType.WITHDRAW,
    "wd": ActionType.WITHDRAW,
    "-": ActionType.WITHDRAW,
    "swap": ActionType.SWAP,
    "s": ActionType.SWAP,
    "=": ActionType.SWAP,
    "limito": ActionType.LIMIT_ORDER,
    "lo": ActionType.LIMIT_ORDER,
    "out": ActionType.OUTBOUND,
    "donate": ActionType.DONATE,
    "d": ActionType.DONATE,
    "bond": ActionType.BOND,
    "unbond": ActionType.UNBOND,
    "leave": ActionType.LEAVE,
    "reserve": ActionType.RESERVE,
    "refund": ActionType.REFUND,
    # "migrate": TxMigrate,
    # "ragnarok": TxRagnarok,
    # "switch": TxType.SWITCH,
    # "noop": TxNoOp,
    # "consolidate": TxConsolidate,
    "name": ActionType.THORNAME,
    "n": ActionType.THORNAME,
    "~": ActionType.THORNAME,
    "$+": ActionType.LOAN_OPEN,
    "loan+": ActionType.LOAN_OPEN,
    "$-": ActionType.LOAN_CLOSE,
    "loan-": ActionType.LOAN_CLOSE,
}


@dataclass
class THORMemo:
    action: ActionType
    asset: str = ''
    dest_address: str = ''
    limit: int = 0
    s_swap_interval: int = 0
    s_swap_quantity: int = 0
    affiliate_address: str = ''
    affiliate_fee_bp: int = 0  # (0..10000) range, may be "node fee" as well in case of "Bond"
    dex_aggregator_address: str = ''
    final_asset_address: str = ''
    min_amount_out: int = 0
    tx_id: str = ''
    withdraw_portion: int = 0
    pool: str = ''
    node_address: str = ''
    node_provider: str = ''
    amount: int = 0
    no_vault: bool = False

    @staticmethod
    def ith_or_default(a, index, default=None, dtype: type = str) -> Union[str, int, float]:
        if 0 <= index < len(a):
            try:
                r = a[index].strip()
                if r == '':
                    return default
                return dtype(r)
            except ValueError:
                return default
        else:
            return default

    @property
    def has_affiliate_part(self):
        return self.affiliate_address and self.affiliate_fee_bp > 0

    @property
    def is_streaming(self):
        return self.s_swap_quantity > 1

    @property
    def uses_aggregator_out(self):
        return bool(self.dex_aggregator_address)

    @classmethod
    def parse_streaming_params(cls, ss: str):
        s_swap_components = ss.split('/')

        limit = cls.ith_or_default(s_swap_components, 0, 0, int)
        s_swap_interval = cls.ith_or_default(s_swap_components, 1, 0, int)
        s_swap_quantity = cls.ith_or_default(s_swap_components, 2, 1, int)
        return limit, s_swap_interval, s_swap_quantity

    @classmethod
    def parse_memo(cls, memo: str):
        gist, *_comment = memo.split('|', maxsplit=2)  # ignore comments

        components = [it for it in gist.split(':')]

        action = cls.ith_or_default(components, 0, '').lower()
        tx_type = MEMO_ACTION_TABLE.get(action)

        if tx_type == ActionType.SWAP.value:
            # 0    1     2        3   4         5   6                   7                8
            # SWAP:ASSET:DESTADDR:LIM:AFFILIATE:FEE:DEX Aggregator Addr:Final Asset Addr:MinAmountOut
            asset = cls.ith_or_default(components, 1)
            dest_address = cls.ith_or_default(components, 2)
            limit_and_s_swap = cls.ith_or_default(components, 3, '')
            limit, s_swap_interval, s_swap_quantity = cls.parse_streaming_params(limit_and_s_swap)

            return cls(
                tx_type, asset, dest_address, limit, s_swap_interval, s_swap_quantity,
                affiliate_address=cls.ith_or_default(components, 4),
                affiliate_fee_bp=cls.ith_or_default(components, 5, 0, dtype=int),
                dex_aggregator_address=cls.ith_or_default(components, 6),
                final_asset_address=cls.ith_or_default(components, 7),
                min_amount_out=cls.ith_or_default(components, 8, 0, dtype=int),
            )
        elif tx_type == ActionType.LOAN_OPEN.value:
            # LOAN+:BTC.BTC:bc1YYYYYY:minBTC:affAddr:affPts:dexAgg:dexTarAddr:DexTargetLimit
            # 0     1       2         3      4       5      6      7          8
            limit_and_s_swap = cls.ith_or_default(components, 3, '')
            limit, s_swap_interval, s_swap_quantity = cls.parse_streaming_params(limit_and_s_swap)
            asset = cls.ith_or_default(components, 1)
            dest_address = cls.ith_or_default(components, 2)

            return cls(
                ActionType.LOAN_OPEN,
                asset,
                dest_address,
                limit,
                s_swap_interval,
                s_swap_quantity,
                affiliate_address=cls.ith_or_default(components, 4),
                affiliate_fee_bp=cls.ith_or_default(components, 5, 0, dtype=int),
                dex_aggregator_address=cls.ith_or_default(components, 6),
                final_asset_address=cls.ith_or_default(components, 7),
                min_amount_out=cls.ith_or_default(components, 8, 0, dtype=int)
            )
        elif tx_type == ActionType.LOAN_CLOSE.value:
            # "LOAN-:BTC.BTC:bc1YYYYYY:minOut"
            #  0     1       2         3

            limit_and_s_swap = cls.ith_or_default(components, 3, '')
            limit, s_swap_interval, s_swap_quantity = cls.parse_streaming_params(limit_and_s_swap)

            asset = cls.ith_or_default(components, 1)
            dest_address = cls.ith_or_default(components, 2)

            return cls(
                ActionType.LOAN_CLOSE, asset, dest_address, limit, s_swap_interval, s_swap_quantity
            )
        elif tx_type == ActionType.WITHDRAW.value:
            # WD:POOL:BASISPOINTS:ASSET
            # 0  1    2           3
            pool = cls.ith_or_default(components, 1, '')
            withdraw_portion = bp_to_float(cls.ith_or_default(components, 2, 0, int))
            asset = cls.ith_or_default(components, 3, '')
            raise cls(
                ActionType.WITHDRAW, pool=pool, withdraw_portion=withdraw_portion, asset=asset
            )
        elif tx_type == ActionType.ADD_LIQUIDITY.value:
            # ADD:POOL:PAIREDADDR:AFFILIATE:FEE
            # 0   1    2          3         4
            pool = cls.ith_or_default(components, 1, '')
            address = cls.ith_or_default(components, 2, '')
            affiliate_address = cls.ith_or_default(components, 3, '')
            affiliate_fee = cls.ith_or_default(components, 4, 0, dtype=int)

            raise cls(
                ActionType.ADD_LIQUIDITY,
                pool=pool, dest_address=address,
                affiliate_address=affiliate_address, affiliate_fee_bp=affiliate_fee
            )
        elif tx_type == ActionType.DONATE.value:
            pool = cls.ith_or_default(components, 1, '')
            return cls(
                ActionType.DONATE, pool=pool
            )
        elif tx_type == ActionType.OUTBOUND.value:
            tx_id = cls.ith_or_default(components, 1, '')
            return cls(
                ActionType.OUTBOUND, tx_id=tx_id
            )
        elif tx_type == ActionType.REFUND.value:
            tx_id = cls.ith_or_default(components, 1, '')
            return cls(
                ActionType.REFUND, tx_id=tx_id
            )
        elif tx_type == ActionType.BOND.value:
            # BOND:NODEADDR:PROVIDER:FEE
            # 0    1        2        3
            node_address = cls.ith_or_default(components, 1, '')
            provider_address = cls.ith_or_default(components, 2, '')
            fee = cls.ith_or_default(components, 3, 0, int)
            return cls(
                ActionType.BOND, node_address=node_address, node_provider=provider_address,
                affiliate_fee_bp=fee
            )
        elif tx_type == ActionType.UNBOND.value:
            # UNBOND:NODEADDR:AMOUNT:PROVIDER
            # 0      1        2      3
            node_address = cls.ith_or_default(components, 1, '')
            amount = cls.ith_or_default(components, 2, 0, int)
            provider_address = cls.ith_or_default(components, 3, '')
            return cls(
                ActionType.UNBOND, node_address=node_address,
                amount=amount, min_amount_out=amount,
            )
        elif tx_type == ActionType.LEAVE.value:
            # LEAVE:NODEADDR
            # 0     1
            node_address = cls.ith_or_default(components, 1, '')
            return cls(ActionType.LEAVE, node_address=node_address)
        elif tx_type == ActionType.RESERVE.value:
            return cls(ActionType.RESERVE)
        elif tx_type == ActionType.NOOP.value:
            no_vault = cls.ith_or_default(components, 1, default='').upper().strip() == 'NOVAULT'
            return cls(ActionType.NOOP, no_vault=no_vault)
        else:
            # todo: parse the rest of types
            raise NotImplementedError(f"Can not parse memo for {tx_type}")

    @property
    def _fee_or_empty(self):
        return str(self.affiliate_fee_bp) if self.affiliate_fee_bp > 0 else ''

    def build(self):
        if self.action == ActionType.ADD_LIQUIDITY:
            memo = ''  # todo
        elif self.action == ActionType.SWAP:
            memo = ''  # todo
        elif self.action == ActionType.WITHDRAW:
            memo = ''  # todo
        elif self.action == ActionType.DONATE:
            memo = ''  # todo
        elif self.action == ActionType.THORNAME:
            memo = ''  # todo
        elif self.action == ActionType.LOAN_OPEN:
            memo = ''  # todo
        elif self.action == ActionType.LOAN_CLOSE:
            memo = ''  # todo

        elif self.action == ActionType.BOND:
            # # BOND:NODEADDR:PROVIDER:FEE
            memo = f'BOND:{self.node_address}:{self.node_provider}:{self._fee_or_empty}'

        elif self.action == ActionType.UNBOND:
            # UNBOND:NODEADDR:AMOUNT:PROVIDER
            memo = f'UNBOND:{self.node_address}:{self.amount}:{self.node_provider}'

        elif self.action == ActionType.LEAVE:
            memo = f"LEAVE:{self.node_address}"

        elif self.action == ActionType.RESERVE:
            memo = 'RESERVE'

        elif self.action == ActionType.OUTBOUND:
            memo = f'OUT:{self.tx_id}'

        elif self.action == ActionType.REFUND:
            memo = f'REFUND:{self.tx_id}'

        elif self.action == ActionType.NOOP:
            memo = 'NOOP:NOVAULT' if self.no_vault else 'NOOP'

        else:
            raise NotImplementedError(f"Can not build memo for {self.action}")

        return memo.strip().rstrip(':')
