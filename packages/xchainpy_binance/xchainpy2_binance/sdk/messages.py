import abc
from collections import OrderedDict
from decimal import Decimal
from typing import List, Dict, Union, Optional, NamedTuple

import binascii
import ujson as json
from cosmpy.crypto.keypairs import PrivateKey

from .constants import TimeInForce, OrderSide, OrderType, VoteOption
from .proto.dex_pb2 import (
    NewOrder, CancelOrder, TokenFreeze, TokenUnfreeze, StdTx, StdSignature, Send, Token, Vote
)
from .utils import varint_encode, decode_address
from .wallet import Account

# An identifier for tools triggering broadcast transactions, set to zero if unwilling to disclose.
BROADCAST_SOURCE = 0


def encode_number(x):
    """
    Does nothing, because parent client will always pass encoded int (8 dec)
    :param x:
    :return:
    """
    return x


class Transfer(NamedTuple):
    amount: Union[int, float, Decimal]
    symbol: str


class Msg(abc.ABC):
    AMINO_MESSAGE_TYPE = ""
    INCLUDE_AMINO_LENGTH_PREFIX = False

    def __init__(self, account: Account, memo: str = ''):
        self.account = account
        self._memo = memo

    def to_dict(self) -> Dict:
        return {}

    def to_sign_dict(self) -> Dict:
        return {}

    @abc.abstractmethod
    def to_protobuf(self):
        pass

    def to_amino(self):
        proto = self.to_protobuf()
        if not isinstance(proto, bytes):
            proto = proto.SerializeToString()

        # wrap with type
        type_bytes = b""
        if self.AMINO_MESSAGE_TYPE:
            type_bytes = binascii.unhexlify(self.AMINO_MESSAGE_TYPE)
            varint_length = varint_encode(len(proto) + len(type_bytes))
        else:
            varint_length = varint_encode(len(proto))

        msg = b""
        if self.INCLUDE_AMINO_LENGTH_PREFIX:
            msg += varint_length
        msg += type_bytes + proto

        return msg

    @property
    def memo(self):
        return self._memo

    def to_hex_data(self):
        """Wrap in a Standard Transaction Message and convert to hex string

        """
        return binascii.hexlify(StdTxMsg(self).to_amino())


class Signature:
    def __init__(self, msg: Msg, data=None, account: Account = None):
        self._msg = msg
        self._data = data
        self._source = BROADCAST_SOURCE
        self._sequence = account.sequence
        self._chain_id = account.chain_id
        self._account_number = account.account_number

    def to_json(self):
        return json.dumps(OrderedDict([
            ('account_number', str(self._account_number)),
            ('chain_id', self._chain_id),
            ('data', self._data),
            ('memo', self._msg.memo),
            ('msgs', [self._msg.to_dict()]),
            ('sequence', str(self._sequence)),
            ('source', str(self._source))
        ]), ensure_ascii=False)

    def to_bytes_json(self):
        return self.to_json().encode()

    def sign(self):
        if not self._msg.account.private_key:
            raise Exception("No private key provided")

        # generate string to sign
        json_bytes = self.to_bytes_json()

        pk = PrivateKey(self._msg.account.private_key)
        signature = pk.sign(json_bytes)
        return signature
        # return signature[-64:]

        # signed = wallet.sign_message(json_bytes)
        # return signed[-64:]


class NewOrderMsg(Msg):
    AMINO_MESSAGE_TYPE = b"CE6DC043"

    def __init__(self, symbol: str, time_in_force: TimeInForce, order_type: OrderType, side: OrderSide,
                 price: Union[int, float, Decimal], quantity: Union[int, float, Decimal],
                 account: Optional[Account] = None):
        """NewOrder transaction creates a new order to buy and sell tokens on Binance DEX.

        :param symbol: symbol for trading pair in full name of the tokens e.g. 'ANN-457_BNB'
        :param time_in_force: TimeInForce type (GOOD_TILL_EXPIRE, IMMEDIATE_OR_CANCEL)
        :param order_type: OrderType (LIMIT, MARKET)
        :param side: OrderSide (BUY, SELL)
        :param price: price of the order e.g. Decimal(0.000396000) or 0.002384
        :param quantity: quantity of the order Decimal(12) or 12

        """
        super().__init__(account)
        self._symbol = symbol
        self._time_in_force = time_in_force.value
        self._order_type = order_type.value
        self._side = side.value
        self._price = price
        self._price_encoded = encode_number(price)
        self._quantity = quantity
        self._quantity_encoded = encode_number(quantity)

    def to_dict(self) -> Dict:
        return OrderedDict([
            ('id', self.account.generate_order_id()),
            ('ordertype', self._order_type),
            ('price', self._price_encoded),
            ('quantity', self._quantity_encoded),
            ('sender', self.account.address),
            ('side', self._side),
            ('symbol', self._symbol),
            ('timeinforce', self._time_in_force),
        ])

    def to_sign_dict(self) -> Dict:
        return {
            'order_type': self._order_type,
            'price': self._price,
            'quantity': self._quantity,
            'side': self._side,
            'symbol': self._symbol,
            'time_in_force': self._time_in_force,
        }

    def to_protobuf(self) -> NewOrder:
        pb = NewOrder()
        # pb.sender = self.account.address_decoded
        pb.sender = self.account.address_bytes
        pb.id = self.account.generate_order_id()
        pb.symbol = self._symbol.encode()
        pb.timeinforce = self._time_in_force
        pb.ordertype = self._order_type
        pb.side = self._side
        pb.price = self._price_encoded
        pb.quantity = self._quantity_encoded
        return pb


class LimitOrderMsg(NewOrderMsg):

    def __init__(self, symbol: str, side: OrderSide,
                 price: Union[int, float, Decimal], quantity: Union[int, float, Decimal],
                 time_in_force: TimeInForce = TimeInForce.GOOD_TILL_EXPIRE,
                 account: Optional[Account] = None):
        """NewOrder transaction creates a new order to buy and sell tokens on Binance DEX.

        :param symbol: symbol for trading pair in full name of the tokens e.g. 'ANN-457_BNB'
        :param side: OrderSide (BUY, SELL)
        :param price: price of the order e.g. Decimal(0.000396000) or 0.002384
        :param quantity: quantity of the order Decimal(12) or 12
        :param time_in_force: TimeInForce type (GOOD_TILL_EXPIRE, IMMEDIATE_OR_CANCEL) default GOOD_TILL_EXPIRE

        """
        super().__init__(
            account=account,
            symbol=symbol,
            time_in_force=time_in_force,
            order_type=OrderType.LIMIT,
            side=side,
            price=price,
            quantity=quantity
        )


class LimitOrderBuyMsg(LimitOrderMsg):

    def __init__(self, symbol: str, price: Union[int, float, Decimal], quantity: Union[int, float, Decimal],
                 time_in_force: TimeInForce = TimeInForce.GOOD_TILL_EXPIRE,
                 account: Optional[Account] = None):
        """LimitOrderBuyMsg transaction creates a new limit order buy message on Binance DEX.

        :param symbol: symbol for trading pair in full name of the tokens e.g. 'ANN-457_BNB'
        :param price: price of the order e.g. Decimal(0.000396000) or 0.002384
        :param quantity: quantity of the order Decimal(12) or 12
        :param time_in_force: TimeInForce type (GOOD_TILL_EXPIRE, IMMEDIATE_OR_CANCEL) default GOOD_TILL_EXPIRE

        """
        super().__init__(
            account=account,
            symbol=symbol,
            time_in_force=time_in_force,
            side=OrderSide.BUY,
            price=price,
            quantity=quantity
        )


class LimitOrderSellMsg(LimitOrderMsg):

    def __init__(self, symbol: str, price: Union[int, float, Decimal], quantity: Union[int, float, Decimal],
                 time_in_force: TimeInForce = TimeInForce.GOOD_TILL_EXPIRE,
                 account: Optional[Account] = None):
        """LimitOrderSellMsg transaction creates a new limit order sell message on Binance DEX.

        :param symbol: symbol for trading pair in full name of the tokens e.g. 'ANN-457_BNB'
        :param time_in_force: TimeInForce type (GOOD_TILL_EXPIRE, IMMEDIATE_OR_CANCEL)
        :param price: price of the order e.g. Decimal(0.000396000) or 0.002384
        :param quantity: quantity of the order Decimal(12) or 12
        :param time_in_force: TimeInForce type (GOOD_TILL_EXPIRE, IMMEDIATE_OR_CANCEL) default GOOD_TILL_EXPIRE

        """
        super().__init__(
            account=account,
            symbol=symbol,
            time_in_force=time_in_force,
            side=OrderSide.SELL,
            price=price,
            quantity=quantity
        )


class CancelOrderMsg(Msg):
    AMINO_MESSAGE_TYPE = b"166E681B"

    def __init__(self, symbol: str, order_id: str, account: Optional[Account] = None):
        """Cancel transactions cancel the outstanding (unfilled) orders from the Binance DEX. After cancel success,
        the locked quantity on the orders would return back to the address' balance and become free to use,
        i.e. transfer or send new orders.

        :param symbol: symbol for trading pair in full name of the tokens
        :param order_id: order id of the one to cancel
        """
        super().__init__(account)

        self._symbol = symbol
        self._order_id = order_id

    def to_dict(self):
        return OrderedDict([
            ('refid', self._order_id),
            ('sender', self.account.address),
            ('symbol', self._symbol),
        ])

    def to_sign_dict(self) -> Dict:
        return {
            'refid': self._order_id,
            'symbol': self._symbol,
        }

    def to_protobuf(self) -> CancelOrder:
        pb = CancelOrder()
        pb.sender = self.account.address_bytes
        pb.refid = self._order_id
        pb.symbol = self._symbol.encode()
        return pb


class FreezeMsg(Msg):
    AMINO_MESSAGE_TYPE = b"E774B32D"

    def __init__(self, symbol: str, amount: Union[int, float, Decimal], account: Optional[Account] = None):
        """Freeze transaction moves the amount of the tokens into a frozen state,
        in which it cannot be used to transfer or send new orders.

        :param symbol: token symbol, in full name with "-" suffix
        :param amount: amount of token to freeze
        """
        super().__init__(account)
        self._symbol = symbol
        self._amount = amount
        self._amount_amino = encode_number(amount)

    def to_dict(self):
        return OrderedDict([
            ('amount', self._amount_amino),
            ('from', self.account.address),
            ('symbol', self._symbol),
        ])

    def to_sign_dict(self) -> Dict:
        return {
            'amount': self._amount,
            'symbol': self._symbol,
        }

    def to_protobuf(self) -> TokenFreeze:
        pb = TokenFreeze()
        setattr(pb, 'from', self.account.address_bytes)
        pb.symbol = self._symbol.encode()
        pb.amount = self._amount_amino
        return pb


class UnFreezeMsg(Msg):
    AMINO_MESSAGE_TYPE = b"6515FF0D"

    def __init__(self, symbol: str, amount: Union[int, float, Decimal], account: Optional[Account] = None):
        """Turn the amount of frozen tokens back to free state.

        :param symbol: token symbol, in full name with "-" suffix
        :param amount: amount of token to unfreeze
        """
        super().__init__(account)
        self._symbol = symbol
        self._amount = amount
        self._amount_amino = encode_number(amount)

    def to_dict(self):
        return OrderedDict([
            ('amount', self._amount_amino),
            ('from', self.account.address),
            ('symbol', self._symbol),
        ])

    def to_sign_dict(self) -> Dict:
        return {
            'amount': self._amount,
            'symbol': self._symbol,
        }

    def to_protobuf(self) -> TokenUnfreeze:
        pb = TokenUnfreeze()
        setattr(pb, 'from', self.account.address_bytes)
        pb.symbol = self._symbol.encode()
        pb.amount = self._amount_amino
        return pb


class SignatureMsg(Msg):
    AMINO_MESSAGE_TYPE = None

    def __init__(self, msg: Msg):
        super().__init__(msg.account)
        self._signature = Signature(msg, account=msg.account)

    def to_protobuf(self) -> StdSignature:
        pub_key_msg = PubKeyMsg(self.account)
        std_sig = StdSignature()
        std_sig.sequence = self.account.sequence
        std_sig.account_number = self.account.account_number
        std_sig.pub_key = pub_key_msg.to_amino()
        std_sig.signature = self._signature.sign()
        return std_sig


class StdTxMsg(Msg):
    AMINO_MESSAGE_TYPE = b"F0625DEE"
    INCLUDE_AMINO_LENGTH_PREFIX = True

    def __init__(self, msg: Msg, data=''):
        super().__init__(msg.account)

        self._msg = msg
        self._signature = SignatureMsg(msg)
        self._data = data
        self._source = BROADCAST_SOURCE

    def to_protobuf(self) -> StdTx:
        stdtx = StdTx()
        stdtx.msgs.extend([self._msg.to_amino()])
        stdtx.signatures.extend([self._signature.to_amino()])
        stdtx.data = self._data.encode()
        stdtx.memo = self._msg.memo
        stdtx.source = self._source
        return stdtx


class PubKeyMsg(Msg):
    AMINO_MESSAGE_TYPE = b"EB5AE987"

    def __init__(self, account: Account):
        super().__init__(account)

    def to_protobuf(self):
        return self.account.public_key

    def to_amino(self):
        proto = self.to_protobuf()

        type_bytes = binascii.unhexlify(self.AMINO_MESSAGE_TYPE)

        varint_length = varint_encode(len(proto))

        msg = type_bytes + varint_length + proto

        return msg


class TransferMsg(Msg):
    AMINO_MESSAGE_TYPE = b"2A2C87FA"

    def __init__(self, symbol: str, amount: Union[int, float, Decimal],
                 to_address: str, account: Optional[Account] = None, memo: str = ''):
        """Transferring funds between different addresses.

        :param symbol: token symbol, in full name with "-" suffix
        :param amount: amount of token to freeze
        :param to_address: amount of token to freeze
        """
        super().__init__(account, memo)
        self._symbol = symbol
        self._amount = amount
        self._amount_amino = encode_number(amount)
        self._from_address = account.address if account else None
        self._to_address = to_address

    def to_dict(self):
        return OrderedDict([
            ('inputs', [
                OrderedDict([
                    ('address', self._from_address),
                    ('coins', [
                        OrderedDict([
                            ('amount', self._amount_amino),
                            ('denom', self._symbol)
                        ])
                    ])
                ])
            ]),
            ('outputs', [
                OrderedDict([
                    ('address', self._to_address),
                    ('coins', [
                        OrderedDict([
                            ('amount', self._amount_amino),
                            ('denom', self._symbol)
                        ])
                    ])
                ])
            ])
        ])

    def to_sign_dict(self):
        return {
            'to_address': self._to_address,
            'amount': self._amount,
            'denom': self._symbol,
        }

    def to_protobuf(self) -> Send:
        token = Send.Token()
        token.denom = self._symbol
        token.amount = self._amount_amino
        input_addr = Send.Input()
        input_addr.address = decode_address(self._from_address)
        input_addr.coins.extend([token])
        output_addr = Send.Output()
        output_addr.address = decode_address(self._to_address)
        output_addr.coins.extend([token])

        msg = Send()
        msg.inputs.extend([input_addr])
        msg.outputs.extend([output_addr])
        return msg

    def to_hex_data(self):
        """Wrap in a Standard Transaction Message and convert to hex string

        """
        return binascii.hexlify(StdTxMsg(self).to_amino())


class MultiTransferMsg(Msg):
    AMINO_MESSAGE_TYPE = b"2A2C87FA"

    def __init__(self, transfers: List[Transfer],
                 to_address: str, account: Optional[Account] = None, memo: str = ''):
        """Transferring funds between different addresses.

        :param transfers: List of tokens and amounts to send
        :param to_address: amount of token to freeze
        """
        super().__init__(account, memo)
        self._transfers = transfers
        self._transfers.sort(key=lambda x: x.symbol)
        self._from_address = account.address if account else None
        self._to_address = to_address

    def to_dict(self):
        return OrderedDict([
            ('inputs', [
                OrderedDict([
                    ('address', self._from_address),
                    ('coins', [
                        OrderedDict([
                            ('amount', encode_number(transfer.amount)),
                            ('denom', transfer.symbol)
                        ]) for transfer in self._transfers
                    ])
                ])
            ]),
            ('outputs', [
                OrderedDict([
                    ('address', self._to_address),
                    ('coins', [
                        OrderedDict([
                            ('amount', encode_number(transfer.amount)),
                            ('denom', transfer.symbol)
                        ]) for transfer in self._transfers
                    ])
                ])
            ])
        ])

    def to_sign_dict(self):
        return {
            'to_address': self._to_address,
            'transfers': [
                {
                    'amount': transfer.amount,
                    'denom': transfer.symbol,
                } for transfer in self._transfers
            ]
        }

    def to_protobuf(self) -> Send:
        input_addr = Send.Input()
        output_addr = Send.Output()
        for transfer in self._transfers:
            token = Token()
            token.denom = transfer.symbol
            token.amount = encode_number(transfer.amount)
            input_addr.coins.extend([token])
            output_addr.coins.extend([token])
        input_addr.address = decode_address(self._from_address)
        output_addr.address = decode_address(self._to_address)

        msg = Send()
        msg.inputs.extend([input_addr])
        msg.outputs.extend([output_addr])
        return msg


class VoteMsg(Msg):
    AMINO_MESSAGE_TYPE = b"A1CADD36"

    VOTE_OPTION_STR = {
        VoteOption.YES: 'Yes',
        VoteOption.ABSTAIN: 'Abstain',
        VoteOption.NO: 'No',
        VoteOption.NO_WITH_VETO: 'NoWithVeto',
    }

    VOTE_OPTION_INT = {
        VoteOption.YES: 1,
        VoteOption.ABSTAIN: 2,
        VoteOption.NO: 3,
        VoteOption.NO_WITH_VETO: 4
    }

    def __init__(self, proposal_id: int, vote_option: VoteOption, account: Optional[Account] = None):
        """Place a vote for a proposal from the given wallet address.

        :param proposal_id: ID of the proposal
        :param vote_option: option chosen by the voter
        """
        super().__init__(account)
        self._proposal_id = proposal_id
        self._proposal_id_amino = encode_number(proposal_id)
        self._voter = account.address if account else None
        self._vote_option = vote_option

    def to_dict(self):
        return OrderedDict([
            ('option', self.VOTE_OPTION_STR[self._vote_option]),
            ('proposal_id', self._proposal_id_amino),
            ('voter', self._voter),
        ])

    def to_sign_dict(self) -> Dict:
        return {
            'proposal_id': self._proposal_id,
            'option': self._vote_option,
        }

    def to_protobuf(self) -> Vote:
        pb = Vote()
        pb.voter = self.account.address_bytes
        pb.proposal_id = self._proposal_id
        pb.option = self.VOTE_OPTION_INT[self._vote_option]
        return pb
