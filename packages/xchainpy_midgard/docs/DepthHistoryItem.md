# DepthHistoryItem

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asset_depth** | **str** | Int64(e8), the amount of Asset in the pool at the end of the interval | 
**asset_price** | **str** | Float, price of asset in rune. I.e. rune amount / asset amount | 
**asset_price_usd** | **str** | Float, the price of asset in USD (based on the deepest USD pool). | 
**close_price_usd** | **str** | Float, the closing price of asset in USD at the end of the interval. | [optional] 
**end_time** | **str** | Int64, The end time of bucket in unix timestamp | 
**high_price_usd** | **str** | Float, the highest price of asset in USD during the interval. | [optional] 
**liquidity_units** | **str** | Int64, Liquidity Units in the pool at the end of the interval | 
**low_price_usd** | **str** | Float, the lowest price of asset in USD during the interval. | [optional] 
**luvi** | **str** | Float, The liquidity unit value index. Sqrt(assetDepth * runeDepth)/liquidity units  | 
**members_count** | **str** | Int64, Number of liquidity members in the pool at the end of the interval | 
**open_price_usd** | **str** | Float, the opening price of asset in USD at the beginning of the interval. | [optional] 
**rune_depth** | **str** | Int64(e8), the amount of Rune in the pool at the end of the interval | 
**start_time** | **str** | Int64, The beginning time of bucket in unix timestamp | 
**synth_supply** | **str** | Int64, Synth supply in the pool at the end of the interval | 
**synth_units** | **str** | Int64, Synth Units in the pool at the end of the interval | 
**units** | **str** | Int64, Total Units (synthUnits + liquidityUnits) in the pool at the end of the interval  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

