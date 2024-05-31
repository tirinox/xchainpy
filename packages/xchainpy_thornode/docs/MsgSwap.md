# MsgSwap

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tx** | [**Tx**](Tx.md) |  | 
**target_asset** | **str** | the asset to be swapped to | 
**destination** | **str** | the destination address to receive the swap output | [optional] 
**trade_target** | **str** | the minimum amount of output asset to receive (else cancelling and refunding the swap) | 
**affiliate_address** | **str** | the affiliate address which will receive any affiliate fee | [optional] 
**affiliate_basis_points** | **str** | the affiliate fee in basis points | 
**signer** | **str** | the signer (sender) of the transaction | [optional] 
**aggregator** | **str** | the contract address if an aggregator is specified for a non-THORChain SwapOut | [optional] 
**aggregator_target_address** | **str** | the desired output asset of the aggregator SwapOut | [optional] 
**aggregator_target_limit** | **str** | the minimum amount of SwapOut asset to receive (else cancelling the SwapOut and receiving THORChain&#x27;s output) | [optional] 
**order_type** | **str** | market if immediately completed or refunded, limit if held until fulfillable | [optional] 
**stream_quantity** | **int** | number of swaps to execute in a streaming swap | [optional] 
**stream_interval** | **int** | the interval (in blocks) to execute the streaming swap | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

