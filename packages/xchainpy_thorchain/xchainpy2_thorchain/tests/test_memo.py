import pytest

from xchainpy2_thorchain.memo import THORMemo, AUTO_OPTIMIZED, ActionType, Affiliate


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
           THORMemo.loan_close('BTC.BTC', BTC_ADDR)

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

    m = THORMemo.loan_open('BTC.BTC', BTC_ADDR, 334343434, affiliates=[
        Affiliate('t', 30), Affiliate('dx', 40), Affiliate(THOR_ADDR_1, 15)
    ])
    assert m.action == ActionType.LOAN_OPEN
    assert m.asset == 'BTC.BTC'
    assert m.dest_address == BTC_ADDR
    assert m.limit == 334343434
    with pytest.raises(ValueError):
        assert m.affiliate_fee_bp
    with pytest.raises(ValueError):
        assert m.affiliate_address

    assert m.affiliates == [
        Affiliate('t', 30), Affiliate('dx', 40), Affiliate(THOR_ADDR_1, 15)
    ]
    assert m.build() == f'$+:BTC.BTC:{BTC_ADDR}:334343434:t/dx/{THOR_ADDR_1}:30/40/15'


FINAL_ETH_ASSET = '0xA0B86991C6218B36C1D19D4A2E9EB0CE3606EB48'
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

    m = THORMemo.thorname_register_or_renew('some_name', 'THOR', THOR_ADDR_1, THOR_ADDR_2, USDC)
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


def test_withdraw():
    m = THORMemo.withdraw(USDC, 10000)
    assert m.action == ActionType.WITHDRAW
    assert m.pool == USDC
    assert m.withdraw_portion_bp == 10000
    assert m.build() == f'-:{USDC}:10000'
    assert THORMemo.parse_memo(f'-:{USDC}:10000') == m

    m = THORMemo.withdraw('BTC.BTC')
    assert m.action == ActionType.WITHDRAW
    assert m.pool == 'BTC.BTC'
    assert m.withdraw_portion_bp == 10000  # default
    assert m.build() == f'-:BTC.BTC:10000'
    assert THORMemo.parse_memo(f'-:BTC.BTC') == m

    m = THORMemo.withdraw('BTC.BTC', 5000, 'RUNE')
    assert m == THORMemo.withdraw_rune('BTC.BTC', 5000)
    assert m.action == ActionType.WITHDRAW
    assert m.pool == 'BTC.BTC'
    assert m.withdraw_portion_bp == 5000
    assert m.asset == 'RUNE'
    assert m.build() == f'-:BTC.BTC:5000:RUNE'
    assert THORMemo.parse_memo(f'-:BTC.BTC:5000:RUNE') == m

    m = THORMemo.withdraw('BTC.BTC', 5000, 'BTC.BTC')
    assert m.action == ActionType.WITHDRAW
    assert m.pool == 'BTC.BTC'
    assert m.withdraw_portion_bp == 5000
    assert m.asset == 'BTC.BTC'
    assert m.build() == f'-:BTC.BTC:5000:BTC.BTC'
    assert THORMemo.parse_memo(f'-:BTC.BTC:5000:BTC.BTC') == m


def test_swap():
    m = THORMemo.swap('ETH.ETH', ETH_ADDR)
    assert m.action == ActionType.SWAP
    assert m.pool == 'ETH.ETH'
    assert m.dest_address == ETH_ADDR
    assert m.refund_address == m.dest_address
    assert m.build() == f'=:ETH.ETH:{ETH_ADDR}'
    assert THORMemo.parse_memo(f'=:ETH.ETH:{ETH_ADDR}') == m

    m = THORMemo.swap('THOR.RUNE', THOR_ADDR_1, 9999999)
    assert m.action == ActionType.SWAP
    assert m.pool == 'THOR.RUNE'
    assert m.dest_address == THOR_ADDR_1
    assert m.refund_address == m.dest_address
    assert m.limit == 9999999
    assert m.build() == f'=:THOR.RUNE:{THOR_ADDR_1}:9999999'
    assert THORMemo.parse_memo(f'=:THOR.RUNE:{THOR_ADDR_1}:9999999') == m

    m = THORMemo.swap('THOR.RUNE', THOR_ADDR_1, 5555, 33, 99)
    assert m.action == ActionType.SWAP
    assert m.pool == 'THOR.RUNE'
    assert m.dest_address == THOR_ADDR_1
    assert m.refund_address == m.dest_address
    assert m.limit == 5555
    assert m.s_swap_interval == 33
    assert m.s_swap_quantity == 99
    assert m.build() == f'=:THOR.RUNE:{THOR_ADDR_1}:5555/33/99'
    assert THORMemo.parse_memo(f'=:THOR.RUNE:{THOR_ADDR_1}:5555/33/99') == m

    m = THORMemo.swap('THOR.RUNE', THOR_ADDR_1, 5555, 33,
                      s_swap_quantity=AUTO_OPTIMIZED,
                      affiliate_address='dx', affiliate_fee_bp=35)
    assert m.action == ActionType.SWAP
    assert m.pool == 'THOR.RUNE'
    assert m.dest_address == THOR_ADDR_1
    assert m.refund_address == m.dest_address
    assert m.limit == 5555
    assert m.s_swap_interval == 33
    assert m.s_swap_quantity == AUTO_OPTIMIZED
    assert m.affiliate_address == 'dx'
    assert m.affiliate_fee_bp == 35
    assert m.build() == f'=:THOR.RUNE:{THOR_ADDR_1}:5555/33/0:dx:35'
    assert THORMemo.parse_memo(f'=:THOR.RUNE:{THOR_ADDR_1}:5555/33/0:dx:35') == m

    m = THORMemo.swap('ETH.ETH', ETH_ADDR, dex_aggregator_address=ETH_ADDR_2,
                      dex_final_asset_address=FINAL_ETH_ASSET, dex_min_amount_out=333888)
    assert m.action == ActionType.SWAP
    assert m.pool == 'ETH.ETH'
    assert m.dest_address == ETH_ADDR
    assert m.refund_address == m.dest_address
    assert m.dex_aggregator_address == ETH_ADDR_2
    assert m.final_asset_address == FINAL_ETH_ASSET
    assert m.min_amount_out == 333888
    assert m.s_swap_interval == 0
    assert m.s_swap_quantity is None
    assert m.build() == f'=:ETH.ETH:{ETH_ADDR}::::{ETH_ADDR_2}:{FINAL_ETH_ASSET}:333888'
    assert THORMemo.parse_memo(f'=:ETH.ETH:{ETH_ADDR}::::{ETH_ADDR_2}:{FINAL_ETH_ASSET}:333888') == m

    m = THORMemo.swap('ETH.ETH', ETH_ADDR, dex_aggregator_address=ETH_ADDR_2,
                      dex_final_asset_address=FINAL_ETH_ASSET, dex_min_amount_out=333888,
                      affiliate_address='t', affiliate_fee_bp=30, limit=9999999, s_swap_interval=4, s_swap_quantity=7)
    assert m.action == ActionType.SWAP
    assert m.pool == 'ETH.ETH'
    assert m.dest_address == ETH_ADDR
    assert m.refund_address == m.dest_address
    assert m.dex_aggregator_address == ETH_ADDR_2
    assert m.final_asset_address == FINAL_ETH_ASSET
    assert m.min_amount_out == 333888
    assert m.limit == 9999999
    assert m.s_swap_interval == 4
    assert m.s_swap_quantity == 7
    assert m.affiliate_address == 't'
    assert m.affiliate_fee_bp == 30
    assert m.build() == f'=:ETH.ETH:{ETH_ADDR}:9999999/4/7:t:30:{ETH_ADDR_2}:{FINAL_ETH_ASSET}:333888'
    assert THORMemo.parse_memo(f'=:ETH.ETH:{ETH_ADDR}:9999999/4/7:t:30:{ETH_ADDR_2}:{FINAL_ETH_ASSET}:333888') == m

    # custom refund address
    m = THORMemo.swap('THOR.RUNE', THOR_ADDR_1, 9873, 33,
                      s_swap_quantity=AUTO_OPTIMIZED,
                      affiliate_address='dx', affiliate_fee_bp=35, refund_address=THOR_ADDR_2)
    assert m.action == ActionType.SWAP
    assert m.pool == 'THOR.RUNE'
    assert m.dest_address == THOR_ADDR_1
    assert m.refund_address == THOR_ADDR_2
    assert m.limit == 9873
    assert m.s_swap_interval == 33
    assert m.s_swap_quantity == AUTO_OPTIMIZED
    assert m.affiliate_address == 'dx'
    assert m.affiliate_fee_bp == 35
    assert m.build() == f'=:THOR.RUNE:{THOR_ADDR_1}/{THOR_ADDR_2}:9873/33/0:dx:35'
    assert THORMemo.parse_memo(f'=:THOR.RUNE:{THOR_ADDR_1}/{THOR_ADDR_2}:9873/33/0:dx:35') == m


def test_add_liquidity():
    m = THORMemo.add_liquidity('ETH.ETH', ETH_ADDR)
    assert m.action == ActionType.ADD_LIQUIDITY
    assert m.pool == 'ETH.ETH'
    assert m.dest_address == ETH_ADDR
    assert m.build() == f'+:ETH.ETH:{ETH_ADDR}'
    assert THORMemo.parse_memo(f'+:ETH.ETH:{ETH_ADDR}') == m

    m = THORMemo.add_liquidity('ETH.ETH', ETH_ADDR, 't', 100)
    assert m.action == ActionType.ADD_LIQUIDITY
    assert m.pool == 'ETH.ETH'
    assert m.dest_address == ETH_ADDR
    assert m.affiliate_address == 't'
    assert m.affiliate_fee_bp == 100
    assert m.build() == f'+:ETH.ETH:{ETH_ADDR}:t:100'
    assert THORMemo.parse_memo(f'+:ETH.ETH:{ETH_ADDR}:t:100') == m

    m = THORMemo.add_savers('ETH/ETH', 't', 100)
    assert m.action == ActionType.ADD_LIQUIDITY
    assert m.pool == 'ETH/ETH'
    assert m.affiliate_address == 't'
    assert m.affiliate_fee_bp == 100
    assert m.build() == f'+:ETH/ETH::t:100'
    assert THORMemo.parse_memo(f'+:ETH/ETH::t:100') == m

    m = THORMemo.add_liquidity('ETH.ETH', ETH_ADDR, affiliates=[
        Affiliate('t', 30), Affiliate('dx', 40), Affiliate(THOR_ADDR_1, 15)
    ])
    assert m.action == ActionType.ADD_LIQUIDITY
    assert m.pool == 'ETH.ETH'
    assert m.dest_address == ETH_ADDR
    assert m.affiliates == [
        Affiliate('t', 30), Affiliate('dx', 40), Affiliate(THOR_ADDR_1, 15)
    ]


def test_trade_asset():
    m = THORMemo.deposit_trade_account(THOR_ADDR_1)
    assert m.action == ActionType.TRADE_ACC_DEPOSIT
    assert m.dest_address == THOR_ADDR_1
    assert m.build() == f'TRADE+:{THOR_ADDR_1}'
    assert THORMemo.parse_memo(f'TRADE+:{THOR_ADDR_1}') == m

    m = THORMemo.withdraw_trade_account(ETH_ADDR)
    assert m.action == ActionType.TRADE_ACC_WITHDRAW
    assert m.dest_address == ETH_ADDR
    assert m.build() == f'TRADE-:{ETH_ADDR}'
    assert THORMemo.parse_memo(f'TRADE-:{ETH_ADDR}') == m

    m = THORMemo.parse_memo('tRaDe-')
    assert m.action == ActionType.TRADE_ACC_WITHDRAW
    assert m.dest_address == ''


def test_memo_runepool():
    m = THORMemo.runepool_add()
    assert m.action == ActionType.RUNEPOOL_ADD
    assert m.build() == 'POOL+'
    assert THORMemo.parse_memo('POOL+') == m
    assert THORMemo.parse_memo('pool+') == m
    assert THORMemo.parse_memo('Pool+') == m

    m = THORMemo.runepool_withdraw(9955, 't', 23)
    assert m.action == ActionType.RUNEPOOL_WITHDRAW
    assert m.withdraw_portion_bp == 9955
    assert m.affiliate_address == 't'
    assert m.affiliate_fee_bp == 23
    assert m.build() == 'POOL-:9955:t:23'

    m = THORMemo.runepool_withdraw(10000)
    assert m.action == ActionType.RUNEPOOL_WITHDRAW
    assert m.withdraw_portion_bp == 10000
    assert m.affiliate_address == ''
    assert m.affiliate_fee_bp == 0
    assert m.build() == 'POOL-:10000'

    m = THORMemo.runepool_withdraw(3344)
    assert m.action == ActionType.RUNEPOOL_WITHDRAW
    assert m.withdraw_portion_bp == 3344
    assert m.affiliate_address == ''
    assert m.affiliate_fee_bp == 0
    assert m.build() == 'POOL-:3344'


def test_multi_affiliates():
    aff3 = [
        Affiliate('t', 30), Affiliate('dx', 40), Affiliate(THOR_ADDR_1, 15)
    ]
    m = THORMemo.swap('ETH.ETH', ETH_ADDR, affiliates=aff3)
    assert m.action == ActionType.SWAP
    assert m.affiliates == aff3
    assert m.build() == f'=:ETH.ETH:{ETH_ADDR}::t/dx/{THOR_ADDR_1}:30/40/15'

    with pytest.raises(ValueError):
        # 6 is too much
        THORMemo.parse_memo(f'=:ETH.ETH:{ETH_ADDR}::a/b/c/d/e/f:1/2/3/4/5/6')

    with pytest.raises(ValueError):
        # 6 is too much
        THORMemo.swap('ETH.ETH', ETH_ADDR, affiliates=[
            Affiliate('a', 1), Affiliate('b', 2), Affiliate('c', 3),
            Affiliate('d', 4), Affiliate('e', 5), Affiliate('f', 6)
        ])

    # same fee for all
    assert THORMemo.parse_memo(f'=:ETH.ETH:{ETH_ADDR}::a/b/c/d:12').affiliates == [
        Affiliate('a', 12), Affiliate('b', 12), Affiliate('c', 12), Affiliate('d', 12)
    ]

    with pytest.raises(ValueError):
        # mismatch of fee collectors and fee bp number
        THORMemo.parse_memo(f'=:ETH.ETH:{ETH_ADDR}::a/b/c/d:14/15')

    with pytest.raises(ValueError):
        # 1234 is too much (1000 is max)
        THORMemo.parse_memo(f'=:ETH.ETH:{ETH_ADDR}::a/b/c/d:14/0/1234/32')

    assert THORMemo.parse_memo(f'=:ETH.ETH:{ETH_ADDR}::a/b/c/d:14///32').affiliates == [
        Affiliate('a', 14), Affiliate('b', 0), Affiliate('c', 0), Affiliate('d', 32)
    ]

    assert THORMemo.parse_memo(f'=:ETH.ETH:{ETH_ADDR}::a/b/c/d:/3//5').affiliates == [
        Affiliate('a', 0), Affiliate('b', 3), Affiliate('c', 0), Affiliate('d', 5)
    ]

    assert THORMemo.swap('ETH.ETH', ETH_ADDR,
                         affiliates=[('a', 1), ('b', 2), ('c', 3), ('d', 4), ('e', 5)]).affiliates == [
               Affiliate('a', 1), Affiliate('b', 2), Affiliate('c', 3),
               Affiliate('d', 4), Affiliate('e', 5)
           ]


def test_tcy():
    m = THORMemo.tcy_claim(ETH_ADDR)
    assert m.action == ActionType.TCY_CLAIM
    assert m.dest_address == ETH_ADDR
    assert m.build() == f'TCY:{ETH_ADDR}'
    assert THORMemo.parse_memo(f'TCY:{ETH_ADDR}') == m

    m = THORMemo.tcy_stake()
    assert m.action == ActionType.TCY_STAKE
    assert m.build() == 'TCY+'
    assert THORMemo.parse_memo('TCY+') == m

    m = THORMemo.tcy_unstake(5891)
    assert m.action == ActionType.TCY_UNSTAKE
    assert m.withdraw_portion_bp == 5891
    assert m.affiliate_address == ''
    assert m.build() == f'TCY-:5891'
    assert THORMemo.parse_memo(f'tcy-:5891') == m
