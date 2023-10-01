# StreamingSwapMeta

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **str** | Int64, Number of swaps events which already happened. | 
**deposited_coin** | [**Coin**](Coin.md) |  | 
**in_coin** | [**Coin**](Coin.md) |  | 
**interval** | **str** | Int64, Number of blocks between swpas. (Blocks/Swap) E.g. 1 means every block. | 
**last_height** | **str** | Int64, The last blockheight the final swap happend (not outbound). This field will be missing until the final swap happens.  | 
**out_coin** | [**Coin**](Coin.md) |  | 
**quantity** | **str** | Int64,  Number of swaps which thorchain is planning to execute. Total count at the end might be less.  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

