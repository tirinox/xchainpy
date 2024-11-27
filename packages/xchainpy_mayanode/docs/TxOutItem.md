# TxOutItem

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**chain** | **str** |  | 
**to_address** | **str** |  | 
**vault_pub_key** | **str** |  | [optional] 
**coin** | [**Coin**](Coin.md) |  | 
**memo** | **str** |  | [optional] 
**max_gas** | [**list[Coin]**](Coin.md) |  | 
**gas_rate** | **int** |  | [optional] 
**in_hash** | **str** |  | [optional] 
**out_hash** | **str** |  | [optional] 
**aggregator** | **str** | the contract address if an aggregator is specified for a non-mayachain SwapOut | [optional] 
**aggregator_target_asset** | **str** | the desired output asset of the aggregator SwapOut | [optional] 
**aggregator_target_limit** | **str** | the minimum amount of SwapOut asset to receive (else cancelling the SwapOut and receiving mayachain&#x27;s output) | [optional] 
**height** | **int** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

