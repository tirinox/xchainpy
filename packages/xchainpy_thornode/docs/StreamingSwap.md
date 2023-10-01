# StreamingSwap

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tx_id** | **str** | the hash of a transaction | [optional] 
**interval** | **int** | how often each swap is made, in blocks | [optional] 
**quantity** | **int** | the total number of swaps in a streaming swaps | [optional] 
**count** | **int** | the amount of swap attempts so far | [optional] 
**last_height** | **int** | the block height of the latest swap | [optional] 
**trade_target** | **str** | the total number of tokens the swapper wants to receive of the output asset | [optional] 
**deposit** | **str** | the number of input tokens the swapper has deposited | [optional] 
**_in** | **str** | the amount of input tokens that have been swapped so far | [optional] 
**out** | **str** | the amount of output tokens that have been swapped so far | [optional] 
**failed_swaps** | **list[int]** | the list of swap indexes that failed | [optional] 
**failed_swap_reasons** | **list[str]** | the list of reasons that sub-swaps have failed | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

