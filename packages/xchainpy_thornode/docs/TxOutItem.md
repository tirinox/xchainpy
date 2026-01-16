# TxOutItem

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**height** | **int** |  | [optional] 
**in_hash** | **str** |  | [optional] 
**out_hash** | **str** |  | [optional] 
**chain** | **str** |  | 
**to_address** | **str** |  | 
**vault_pub_key** | **str** |  | [optional] 
**vault_pub_key_eddsa** | **str** |  | [optional] 
**coin** | [**Coin**](Coin.md) |  | 
**max_gas** | [**list[Coin]**](Coin.md) |  | 
**gas_rate** | **int** |  | [optional] 
**memo** | **str** |  | [optional] 
**aggregator** | **str** | whitelisted DEX Aggregator contract address | [optional] 
**aggregator_target_asset** | **str** | target asset for the aggregator contract to attempt a swap to | [optional] 
**aggregator_target_limit** | **str** | the minimum number of tokens the swapper wants to receive of the output asset | [optional] 
**clout_spent** | **str** | clout spent in RUNE for the outbound | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

