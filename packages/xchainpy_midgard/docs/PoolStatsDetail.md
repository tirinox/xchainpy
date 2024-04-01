# PoolStatsDetail

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**add_asset_liquidity_volume** | **str** | Int64(e8), same as history/liquidity_changes:addAssetLiquidityVolume | 
**add_liquidity_count** | **str** | Int64, same as history/liquidity_changes:addLiquidityCount | 
**add_liquidity_volume** | **str** | Int64(e8), same as history/liquidity_changes:addLiquidityVolume | 
**add_rune_liquidity_volume** | **str** | Int64(e8), same as history/liquidity_changes:addRuneLiquidityVolume | 
**annual_percentage_rate** | **str** | deprecated now it&#x27;s only showing zero util being deleted. | 
**asset** | **str** |  | 
**asset_depth** | **str** | Int64(e8), the amount of Asset in the pool | 
**asset_price** | **str** | Float, price of asset in rune. I.e. rune amount / asset amount | 
**asset_price_usd** | **str** | Float, the price of asset in USD (based on the deepest USD pool). | 
**average_slip** | **str** | Float64 (Basis points, 0-10000, where 10000&#x3D;100%), same as history/swaps:averageSlip  | 
**earnings** | **str** | Int64(e8), The earning that has been recorded from the pool asset&#x27;s Liquidity Fees and Rewards in RUNE. The earnings shown are from the period parameter default being 14 days  (configurable by the period parameter).  | 
**earnings_annual_as_percent_of_depth** | **str** | Float, The estimation of earnings during the time interval expanded through a year  compared to the current pool depth. E.g. 0.1 means the pool based on this interval earnings can earn 10% of its pool during a year.  | 
**liquidity_units** | **str** | Int64, Liquidity Units in the pool | 
**pool_apy** | **str** | deprecated now it&#x27;s only showing zero util being deleted. | 
**rune_depth** | **str** | Int64(e8), the amount of Rune in the pool | 
**savers_apr** | **str** | Float, Annual Return estimated linearly (not compounded) for savers from a period of typically the last 30 or 100 days (configurable by the period parameter, default is 14). E.g. 0.1 means 10% yearly return. If the savers period has not yet been reached, It will show zero instead.  | 
**status** | **str** | The state of the pool, e.g. Available, Staged | 
**swap_count** | **str** | Int64, same as history/swaps:totalCount | 
**swap_volume** | **str** | Int64(e8), same as history/swaps:totalVolume | 
**synth_supply** | **str** | Int64, Synth supply in the pool | 
**synth_units** | **str** | Int64, Synth Units in the pool | 
**to_asset_average_slip** | **str** | Float64 (Basis points, 0-10000, where 10000&#x3D;100%), same as history/swaps:toAssetAverageSlip  | 
**to_asset_count** | **str** | Int64, same as history/swaps:toAssetCount | 
**to_asset_fees** | **str** | Int64(e8), same as history/swaps:toAssetFees | 
**to_asset_volume** | **str** | Int64(e8), same as history/swaps:toAssetVolume | 
**to_rune_average_slip** | **str** | Float64 (Basis points, 0-10000, where 10000&#x3D;100%), same as history/swaps:toRuneAverageSlip  | 
**to_rune_count** | **str** | Int64, same as history/swaps:toRuneCount | 
**to_rune_fees** | **str** | Int64(e8), same as history/swaps:toRuneFees | 
**to_rune_volume** | **str** | Int64(e8), same as history/swaps:toRuneVolume | 
**total_fees** | **str** | Int64(e8), same as history/swaps:totalFees | 
**unique_member_count** | **str** | Int64, same as len(history/members?pool&#x3D;POOL) | 
**unique_swapper_count** | **str** | Deprecated, it&#x27;s always 0. | 
**units** | **str** | Int64, Total Units (synthUnits + liquidityUnits) in the pool | 
**withdraw_asset_volume** | **str** | Int64(e8), same as history/liquidity_changes:withdrawAssetVolume | 
**withdraw_count** | **str** | Int64, same as history/liquidity_changes:withdrawCount | 
**withdraw_rune_volume** | **str** | Int64(e8), same as history/liquidity_changes:withdrawRuneVolume | 
**withdraw_volume** | **str** | Int64(e8), same as history/liquidity_changes:withdrawVolume | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

