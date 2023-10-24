import pytest

from xchainpy2_thorchain_amm import ActionType
from xchainpy2_thorchain_amm.memo import THORMemo


def test_invalid_memo():
    assert THORMemo.parse_memo('foo:bar:123', no_raise=True) is None
    with pytest.raises(NotImplementedError):
        assert THORMemo.parse_memo('baobab:palm')


def test_noop():
    n1 = THORMemo.noop()
    assert n1.action == ActionType.NOOP
    assert not n1.no_vault
    assert n1.build() == 'NOOP'

    n2 = THORMemo.noop(True)
    assert n2.action == ActionType.NOOP
    assert n2.no_vault
    assert n2.build() == 'NOOP:NOVAULT'

    assert THORMemo.parse_memo('noop') == n1
    assert THORMemo.parse_memo('NOOP') == n1
    assert THORMemo.parse_memo('nOoP') == n1
    assert THORMemo.parse_memo('nOoP:abra') == n1

    assert THORMemo.parse_memo('nOoP:novault') == n2
    assert THORMemo.parse_memo('NOOP:NOVAULT') == n2
    assert THORMemo.parse_memo('Noop:NoVault') == n2


def test_reserve():
    memo = THORMemo.reserve()
    assert memo.build() == 'RESERVE'
    assert memo.action == ActionType.RESERVE

    assert THORMemo.parse_memo('reserve') == memo


TX_ID = '12345679123456789AABB434434DDE11ADA'


def test_out():
    o = THORMemo.outbound(TX_ID)
    assert o.action == ActionType.OUTBOUND
    assert o.tx_id == TX_ID

    assert o.build() == f'OUT:{TX_ID}'

    assert THORMemo.parse_memo(f'OUT:{TX_ID}') == o
    assert THORMemo.parse_memo('OUT:123') == THORMemo.outbound('123')
    assert THORMemo.parse_memo('OUT:') == THORMemo.outbound('')


def test_refund():
    o = THORMemo.refund(TX_ID)
    assert o.action == ActionType.REFUND
    assert o.tx_id == TX_ID

    assert o.build() == f'REFUND:{TX_ID}'

    assert THORMemo.parse_memo(f'REFUND:{TX_ID}') == o
    assert THORMemo.parse_memo('REFUND:123') == THORMemo.refund('123')
    assert THORMemo.parse_memo('REFUND:') == THORMemo.refund('')


THOR_ADDR_1 = 'thor1dl7un46w7l7f3ewrnrm6nq58nerjtp0dradjtd'
THOR_ADDR_2 = 'thor104gsqwta048e80j909g6y9kkqdjrw0lff866ew'


def test_leave():
    memo = THORMemo.leave(THOR_ADDR_1)

    assert memo.action == ActionType.LEAVE
    assert memo.node_address == THOR_ADDR_1

    assert memo.build() == f'LEAVE:{THOR_ADDR_1}'

    assert THORMemo.parse_memo(f'LEAVE:{THOR_ADDR_1}') == memo


def test_unbond():
    u = THORMemo.unbond(THOR_ADDR_1, 1234567890, THOR_ADDR_2)

    assert u.action == ActionType.UNBOND
    assert u.node_address == THOR_ADDR_1
    assert u.provider_address == THOR_ADDR_2
    assert u.amount == 1234567890

    assert u.build() == f'UNBOND:{THOR_ADDR_1}:1234567890:{THOR_ADDR_2}'
    assert THORMemo.parse_memo(f'unbond:{THOR_ADDR_1}:1234567890:{THOR_ADDR_2}') == u

    u2 = THORMemo.unbond(THOR_ADDR_1, 777)
    assert u2.action == ActionType.UNBOND
    assert u2.node_address == THOR_ADDR_1
    assert u2.provider_address == ''
    assert u2.build() == f'UNBOND:{THOR_ADDR_1}:777'

    assert THORMemo.parse_memo('UNBOND:foo:5:bar') == THORMemo.unbond('foo', 5, 'bar')

    # todo: should it raise an exception?
    assert THORMemo.parse_memo('UNBOND:foo:non_number:bar') == THORMemo.unbond('foo', 0, 'bar')


def text_bond():
    u = THORMemo.bond(THOR_ADDR_1, THOR_ADDR_2, 200)

    assert u.action == ActionType.UNBOND
    assert u.node_address == THOR_ADDR_1
    assert u.provider_address == THOR_ADDR_2
    assert u.affiliate_fee_bp == 200

    assert u.build() == f'BOND:{THOR_ADDR_1}:{THOR_ADDR_2}:200'
    assert THORMemo.parse_memo(f'bond:{THOR_ADDR_1}:{THOR_ADDR_2}:200') == u

    # no fee
    u = THORMemo.bond(THOR_ADDR_1, THOR_ADDR_2)
    assert u.build() == f'BOND:{THOR_ADDR_1}:{THOR_ADDR_2}'
    assert THORMemo.parse_memo(f'bond:{THOR_ADDR_1}:{THOR_ADDR_2}') == u

    # todo: should it raise?
    assert THORMemo.parse_memo(f'bond:{THOR_ADDR_1}:{THOR_ADDR_2}:foo') == u

    # just node
    u = THORMemo.bond(THOR_ADDR_1)
    assert u.build() == f'BOND:{THOR_ADDR_1}'
    assert THORMemo.parse_memo(f'BOND:{THOR_ADDR_1}') == u


ETH_ADDR = '0x1c7b17362c84287bd1184447e6dfeaf920c31bbe'
ETH_ADDR_2 = '0xe9973cb51ee04446a54ffca73446d33f133d2f49'
BTC_ADDR = 'bc1qp2t4hl4jr6wjfzv28tsdyjysw7p5armf7px55w'


def test_loan_close():
    m = THORMemo.loan_close('ETH.ETH', ETH_ADDR, 1000)
    assert m.action == ActionType.LOAN_CLOSE
    assert m.asset == 'ETH.ETH'
    assert m.dest_address == ETH_ADDR

    assert m.build() == f'$-:ETH.ETH:{ETH_ADDR}:1000'

    assert THORMemo.parse_memo(f'Loan-:ETH.ETH:{ETH_ADDR}:1000') == m
    assert THORMemo.parse_memo(f'$-:ETH.ETH:{ETH_ADDR}:1000') == m

    m = THORMemo.loan_close('ETH.ETH', ETH_ADDR)
    assert m.action == ActionType.LOAN_CLOSE
    assert m.asset == 'ETH.ETH'
    assert m.dest_address == ETH_ADDR
    assert m.build() == f'$-:ETH.ETH:{ETH_ADDR}'

    assert THORMemo.parse_memo(f'$-:BTC.BTC:{BTC_ADDR}') == \
           THORMemo.loan_close('BTC.BTC', BTC_ADDR, 0)

    assert THORMemo.parse_memo(f'LOAN-:ETH.ETH:{ETH_ADDR_2}:404204059') == \
           THORMemo.loan_close('ETH.ETH', ETH_ADDR_2, 404204059)

    assert THORMemo.parse_memo(f'LOAN-:ETH.ETH:{ETH_ADDR_2}:404e8') == \
           THORMemo.loan_close('ETH.ETH', ETH_ADDR_2, 40400000000)


def test_loan_open():
    m = THORMemo.loan_open('BTC.BTC', BTC_ADDR, 282392832)
    assert m.action == ActionType.LOAN_OPEN
    assert m.asset == 'BTC.BTC'
    assert m.dest_address == BTC_ADDR
    assert m.limit == 282392832
    assert m.affiliate_fee_bp == 0
    assert m.affiliate_address == ''

    assert m.build() == f'$+:BTC.BTC:{BTC_ADDR}:282392832'
    assert THORMemo.parse_memo(f'$+:BTC.BTC:{BTC_ADDR}:282392832') == m

    m = THORMemo.loan_open('ETH.ETH', ETH_ADDR, 404204059, 't', 30)
    assert m.action == ActionType.LOAN_OPEN
    assert m.asset == 'ETH.ETH'
    assert m.dest_address == ETH_ADDR
    assert m.limit == 404204059
    assert m.affiliate_fee_bp == 30
    assert m.affiliate_address == 't'
    assert m.dex_aggregator_address == ''
    assert m.min_amount_out == 0
    assert m.final_asset_address == ''

    assert m.build() == f'$+:ETH.ETH:{ETH_ADDR}:404204059:t:30'

    assert THORMemo.parse_memo(f'Loan+:ETH.ETH:{ETH_ADDR}:404204059:t:30') == m
    assert THORMemo.parse_memo(f'$+:ETH.ETH:{ETH_ADDR}:404204059:t:30') == m


USDC = 'ETH.USDC-0XA0B86991C6218B36C1D19D4A2E9EB0CE3606EB48'


def test_thor_name():
    m = THORMemo.thorname_register_or_renew('foo', 'THOR', THOR_ADDR_1)
    assert m.action == ActionType.THORNAME
    assert m.name == 'foo'
    assert m.chain == 'THOR'
    assert m.dest_address == THOR_ADDR_1
    assert m.build() == f'~:foo:THOR:{THOR_ADDR_1}'
    assert THORMemo.parse_memo(f'~:foo:THOR:{THOR_ADDR_1}') == m

    m = THORMemo.thorname_register_or_renew('acc-test', 'THOR', THOR_ADDR_1, THOR_ADDR_2)
    assert m.action == ActionType.THORNAME
    assert m.name == 'acc-test'
    assert m.chain == 'THOR'
    assert m.dest_address == THOR_ADDR_1
    assert m.owner == THOR_ADDR_2
    assert m.build() == f'~:acc-test:THOR:{THOR_ADDR_1}:{THOR_ADDR_2}'
    assert THORMemo.parse_memo(f'N:acc-test:THOR:{THOR_ADDR_1}:{THOR_ADDR_2}') == m

    m = THORMemo.thorname_set_preferred('some_name', 'THOR', THOR_ADDR_1, USDC, THOR_ADDR_2)
    assert m.action == ActionType.THORNAME
    assert m.name == 'some_name'
    assert m.chain == 'THOR'
    assert m.dest_address == THOR_ADDR_1
    assert m.owner == THOR_ADDR_2
    assert m.affiliate_asset == USDC
    assert m.build() == f'~:some_name:THOR:{THOR_ADDR_1}:{THOR_ADDR_2}:{USDC}'
    assert THORMemo.parse_memo(f'~:some_name:THOR:{THOR_ADDR_1}:{THOR_ADDR_2}:{USDC}') == m
    assert THORMemo.parse_memo(f'name:some_name:THOR:{THOR_ADDR_1}:{THOR_ADDR_2}:{USDC}') == m


def test_donate():
    m = THORMemo.donate(USDC)
    assert m.action == ActionType.DONATE
    assert m.asset == USDC
    assert m.build() == f'DONATE:{USDC}'
    assert THORMemo.parse_memo(f'DONATE:{USDC}') == m
    assert THORMemo.parse_memo(f'donate:{USDC}') == m
    assert THORMemo.parse_memo(f'd:{USDC}') == m

