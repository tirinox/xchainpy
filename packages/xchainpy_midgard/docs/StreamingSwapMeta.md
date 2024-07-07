# StreamingSwapMeta

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **str** | Int64, Number of swaps events which already happened. | 
**deposited_coin** | [**Coin**](Coin.md) |  | 
**failed_swap_reasons** | **list[str]** | Array of failed swaps reasons in streaming swap. | [optional] 
**failed_swaps** | **list[str]** | Array of failed swaps index in streaming swap. | [optional] 
**in_coin** | [**Coin**](Coin.md) |  | 
**interval** | **str** | Int64, Number of blocks between swpas. (Blocks/Swap) E.g. 1 means every block. | 
**last_height** | **str** | Int64, The last blockheight the final swap happened (not outbound). This field will be missing until the final swap happens.  | 
**out_coin** | [**Coin**](Coin.md) |  | 
**quantity** | **str** | Int64,  Number of swaps which thorchain is planning to execute. Total count at the end might be less.  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

