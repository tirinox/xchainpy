# SwapHistoryItem

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**average_slip** | **str** | Float64 (Basis points, 0-10000, where 10000&#x3D;100%), the weighted average (by count) of toAssetAverageSlip, toRuneAverageSlip, synthMintAverageSlip, synthRedeemAverageSlip. Big swaps have the same weight as small swaps.  | 
**end_time** | **str** | Int64, The end time of bucket in unix timestamp | 
**from_trade_average_slip** | **str** | Float64 (Basis points, 0-10000, where 10000&#x3D;100%), the average slip for swaps from asset to trade asset. Big swaps have the same weight as small swaps  | 
**from_trade_count** | **str** | Int64, count of swaps from trade asset to rune | 
**from_trade_fees** | **str** | Int64(e8), the fees collected from swaps from rune to trade asset (in rune) | 
**from_trade_volume** | **str** | Int64(e8), volume of swaps from rune to trade asset denoted in rune | 
**from_trade_volume_usd** | **str** | Int64(e2), volume of swaps from trade asset to rune denoted in USD price of the rune in each swap | 
**rune_price_usd** | **str** | Float, the price of Rune based on the deepest USD pool at the end of the interval.  | 
**start_time** | **str** | Int64, The beginning time of bucket in unix timestamp | 
**synth_mint_average_slip** | **str** | Float64 (Basis points, 0-10000, where 10000&#x3D;100%), the average slip for swaps from rune to synthetic asset. Big swaps have the same weight as small swaps  | 
**synth_mint_count** | **str** | Int64, count of rune to synthetic asset swaps | 
**synth_mint_fees** | **str** | Int64(e8), the fees collected from swaps from rune to synthetic asset (in rune)  | 
**synth_mint_volume** | **str** | Int64(e8), volume of swaps from rune to synthetic asset denoted in rune | 
**synth_mint_volume_usd** | **str** | Int64(e2), volume of swaps from rune to synthetic asset denoted in USD price of the rune in each swap | 
**synth_redeem_average_slip** | **str** | Float64 (Basis points, 0-10000, where 10000&#x3D;100%), the average slip for swaps from synthetic asset to rune. Big swaps have the same weight as small swaps  | 
**synth_redeem_count** | **str** | Int64, count of synthetic asset to rune swaps | 
**synth_redeem_fees** | **str** | Int64(e8), the fees collected from swaps from synthetic asset to rune (in rune)  | 
**synth_redeem_volume** | **str** | Int64(e8), volume of swaps from synthetic asset to rune denoted in rune | 
**synth_redeem_volume_usd** | **str** | Int64(e2), volume of swaps from synthetic asset to rune denoted in USD price of the rune in each swap | 
**to_asset_average_slip** | **str** | Float64 (Basis points, 0-10000, where 10000&#x3D;100%), the average slip for swaps from rune to asset. Big swaps have the same weight as small swaps  | 
**to_asset_count** | **str** | Int64, count of swaps from rune to asset | 
**to_asset_fees** | **str** | Int64(e8), the fees collected from swaps from rune to asset (in rune) | 
**to_asset_volume** | **str** | Int64(e8), volume of swaps from rune to asset denoted in rune | 
**to_asset_volume_usd** | **str** | Int64(e2), volume of swaps from rune to asset denoted in USD price of the rune in each swap | 
**to_rune_average_slip** | **str** | Float64 (Basis points, 0-10000, where 10000&#x3D;100%), the average slip for swaps from asset to rune. Big swaps have the same weight as small swaps  | 
**to_rune_count** | **str** | Int64, count of swaps from asset to rune | 
**to_rune_fees** | **str** | Int64(e8), the fees collected from swaps from asset to rune (in rune) | 
**to_rune_volume** | **str** | Int64(e8), volume of swaps from asset to rune denoted in rune | 
**to_rune_volume_usd** | **str** | Int64(e2), volume of swaps from asset to rune denoted in USD price of the rune in each swap | 
**to_trade_average_slip** | **str** | Float64 (Basis points, 0-10000, where 10000&#x3D;100%), the average slip for swaps from rune to trade asset. Big swaps have the same weight as small swaps  | 
**to_trade_count** | **str** | Int64, count of swaps from rune to trade asset | 
**to_trade_fees** | **str** | Int64(e8), the fees collected from swaps from rune to trade asset (in rune) | 
**to_trade_volume** | **str** | Int64(e8), volume of swaps from trade asset to rune denoted in rune | 
**to_trade_volume_usd** | **str** | Int64(e2), volume of swaps from rune to trade asset denoted in USD price of the rune in each swap | 
**total_count** | **str** | Int64, toAssetCount + toRuneCount + synthMintCount + synthRedeemCount | 
**total_fees** | **str** | Int64(e8), toAssetFees + toRuneFees + synthMintFees + synthRedeemFees | 
**total_volume** | **str** | Int64(e8), toAssetVolume + toRuneVolume + synthMintVolume + synthRedeemVolume (denoted in rune)  | 
**total_volume_usd** | **str** | Int64(e2), toAssetVolume + toRuneVolume + synthMintVolume + synthRedeemVolume (denoted in USD price of the rune in each swap)  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

