# ObservedTx

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tx** | [**Tx**](Tx.md) |  | 
**status** | **str** |  | [optional] 
**out_hashes** | **list[str]** |  | [optional] 
**block_height** | **int** | the block height of the observed transaction on the source chain, not provided if chain is MAYA | [optional] 
**signers** | **list[str]** |  | [optional] 
**observed_pub_key** | **str** |  | [optional] 
**keysign_ms** | **int** |  | [optional] 
**finalise_height** | **int** | the finalised height of the observed transaction on the source chain, not provided if chain is MAYA | [optional] 
**aggregator** | **str** | the outbound aggregator to use, will also match a suffix | [optional] 
**aggregator_target** | **str** | the aggregator target asset provided to transferOutAndCall | [optional] 
**aggregator_target_limit** | **str** | the aggregator target asset limit provided to transferOutAndCall | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

