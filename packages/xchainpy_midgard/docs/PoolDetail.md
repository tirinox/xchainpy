# PoolDetail

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**annual_percentage_rate** | **str** | Float, Also called APR. Annual return estimated linearly (not compounded) from a period of typically the last 30 or 100 days (configurable by the period parameter, default is 30). E.g. 0.1 means 10% yearly return. Due to Impermanent Loss and Synths this might be negative, but given Impermanent Loss Protection for 100+ day members, frontends might show MAX(APR, 0).  | 
**asset** | **str** |  | 
**asset_depth** | **str** | Int64(e8), the amount of Asset in the pool. | 
**asset_price** | **str** | Float, price of asset in rune. I.e. rune amount / asset amount. | 
**asset_price_usd** | **str** | Float, the price of asset in USD (based on the deepest USD pool). | 
**liquidity_units** | **str** | Int64, Liquidity Units in the pool. | 
**pool_apy** | **str** | Float, MAX(AnnualPercentageRate, 0)  | 
**rune_depth** | **str** | Int64(e8), the amount of Rune in the pool. | 
**status** | **str** | The state of the pool, e.g. Available, Staged. | 
**synth_supply** | **str** | Int64, Synth supply in the pool. | 
**synth_units** | **str** | Int64, Synth Units in the pool. | 
**units** | **str** | Int64, Total Units (synthUnits + liquidityUnits) in the pool. | 
**volume24h** | **str** | Int64(e8), the total volume of swaps in the last 24h to and from Rune denoted in Rune. It includes synth mint or burn.  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

