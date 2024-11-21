
from xchainpy2_thornode import Pool

BUSD_POOL = Pool(
    pool_units=52543071634074,
    asset='BNB.BUSD-BD1',
    balance_asset=377399468483592,
    balance_rune=250518706651581,
    pending_inbound_asset=280314005423,
    pending_inbound_rune=533139903979,
    lp_units=56086787104869,
    savers_depth=0,
    savers_units=0,
    status='Available',
    synth_mint_paused=False,
    synth_supply=47690245926711,
    synth_supply_remaining=329709222556881,
    synth_units=3543715470795,
    derived_depth_bps='',
    loan_collateral='',
    loan_cr='',
    loan_collateral_remaining=1,
    asset_tor_price=1.0,
    savers_fill_bps=3323,
    savers_capacity_remaining=3323232,
)

def test_pool_ownership():
    ...