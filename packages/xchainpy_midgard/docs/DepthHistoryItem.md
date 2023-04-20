# DepthHistoryItem

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asset_depth** | **str** | Int64(e8), the amount of Asset in the pool at the end of the interval | 
**asset_price** | **str** | Float, price of asset in rune. I.e. rune amount / asset amount | 
**asset_price_usd** | **str** | Float, the price of asset in USD (based on the deepest USD pool). | 
**end_time** | **str** | Int64, The end time of bucket in unix timestamp | 
**liquidity_units** | **str** | Int64, Liquidity Units in the pool at the end of the interval | 
**luvi** | **str** | Float, The liquidity unit value index. Sqrt(assetDepth * runeDepth)/liquidity units  | 
**rune_depth** | **str** | Int64(e8), the amount of Rune in the pool at the end of the interval | 
**start_time** | **str** | Int64, The beginning time of bucket in unix timestamp | 
**synth_supply** | **str** | Int64, Synth supply in the pool at the end of the interval | 
**synth_units** | **str** | Int64, Synth Units in the pool at the end of the interval | 
**units** | **str** | Int64, Total Units (synthUnits + liquidityUnits) in the pool at the end of the interval  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

