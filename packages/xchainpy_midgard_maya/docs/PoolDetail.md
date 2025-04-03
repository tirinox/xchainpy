# PoolDetail

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**annual_percentage_rate** | **str** | Float, Also called APR. Annual return estimated linearly (not compounded) from a period of typically the last 30 or 100 days (configurable by the period parameter, default is 30). E.g. 0.1 means 10% yearly return. Due to Impermanent Loss and Synths this might be negative, but given Impermanent Loss Protection for 100+ day members, frontends might show MAX(APR, 0).  | 
**asset** | **str** |  | 
**asset_depth** | **str** | Int64(e8), the amount of Asset in the pool. | 
**asset_price** | **str** | Float, price of asset in rune. I.e. rune amount / asset amount. | 
**asset_price_usd** | **str** | Float, the price of asset in USD (based on the deepest USD pool). | 
**earnings** | **str** | Int64(e8), The earning that has been recorded from the pool asset&#x27;s Liquidity Fees and Rewards in RUNE. The earnings shown are from the period parameter default being 14 days  (configurable by the period parameter).  | 
**earnings_annual_as_percent_of_depth** | **str** | Float, The estimation of earnings during the time interval expanded through a year  compared to the current pool depth. E.g. 0.1 means the pool based on this interval earnings can earn 10% of its pool during a year.  | 
**liquidity_units** | **str** | Int64, Liquidity Units in the pool. | 
**native_decimal** | **str** | Int64, The native decimal number of the pool asset. (If the value is \&quot;-1\&quot;, it means midgard doesn&#x27;t know the pool native decimal) | 
**pool_apy** | **str** | Float, MAX(AnnualPercentageRate, 0)  | 
**rune_depth** | **str** | Int64(e8), the amount of Rune in the pool. | 
**savers_apr** | **str** | Float, Annual Return estimated linearly (not compounded) for savers from a period of typically the last 30 or 100 days (configurable by the period parameter, default is 30). E.g. 0.1 means 10% yearly return. If the savers period has not yet been reached, It will show zero instead.  | 
**savers_depth** | **str** | Int64, Total synth locked in saver vault. | 
**savers_units** | **str** | Int64, Units tracking savers vault ownership. | 
**status** | **str** | The state of the pool, e.g. Available, Staged. | 
**synth_supply** | **str** | Int64, Synth supply in the pool. | 
**synth_units** | **str** | Int64, Synth Units in the pool. | 
**total_collateral** | **str** | Int64, Total collateral of the pool created by the borrowers. | 
**total_debt_tor** | **str** | Int64, Total debt of the pool by the borrowers. | 
**units** | **str** | Int64, Total Units (synthUnits + liquidityUnits) in the pool. | 
**volume24h** | **str** | Int64(e8), the total volume of swaps in the last 24h to and from Rune denoted in Rune. It includes synth mint or burn.  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

