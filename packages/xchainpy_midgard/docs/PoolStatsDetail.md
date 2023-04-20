# PoolStatsDetail

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**add_asset_liquidity_volume** | **str** | Int64(e8), same as history/liquidity_changes:addAssetLiquidityVolume | 
**add_liquidity_count** | **str** | Int64, same as history/liquidity_changes:addLiquidityCount | 
**add_liquidity_volume** | **str** | Int64(e8), same as history/liquidity_changes:addLiquidityVolume | 
**add_rune_liquidity_volume** | **str** | Int64(e8), same as history/liquidity_changes:addRuneLiquidityVolume | 
**annual_percentage_rate** | **str** | Float, Also called APR. Annual return estimated linearly (not compounded) from a period of typically the last 30 or 100 days (configurable by the period parameter, default is 30). E.g. 0.1 means 10% yearly return. Due to Impermanent Loss and Synths this might be negative, but given Impermanent Loss Protection for 100+ day members, frontends might show MAX(APR, 0).  | 
**asset** | **str** |  | 
**asset_depth** | **str** | Int64(e8), the amount of Asset in the pool | 
**asset_price** | **str** | Float, price of asset in rune. I.e. rune amount / asset amount | 
**asset_price_usd** | **str** | Float, the price of asset in USD (based on the deepest USD pool). | 
**average_slip** | **str** | Float64 (Basis points, 0-10000, where 10000&#x3D;100%), same as history/swaps:averageSlip  | 
**impermanent_loss_protection_paid** | **str** | Int64(e8), part of the withdrawRuneVolume which was payed because of impermanent loss protection.  | 
**liquidity_units** | **str** | Int64, Liquidity Units in the pool | 
**pool_apy** | **str** | Float, MAX(AnnualPercentageRate, 0)  | 
**rune_depth** | **str** | Int64(e8), the amount of Rune in the pool | 
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

