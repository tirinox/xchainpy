# ObservedTx

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tx** | [**Tx**](Tx.md) |  | 
**observed_pub_key** | **str** |  | [optional] 
**external_observed_height** | **int** | the block height on the external source chain when the transaction was observed, not provided if chain is THOR | [optional] 
**external_confirmation_delay_height** | **int** | the block height on the external source chain when confirmation counting will be complete, not provided if chain is THOR | [optional] 
**aggregator** | **str** | the outbound aggregator to use, will also match a suffix | [optional] 
**aggregator_target** | **str** | the aggregator target asset provided to transferOutAndCall | [optional] 
**aggregator_target_limit** | **str** | the aggregator target asset limit provided to transferOutAndCall | [optional] 
**signers** | **list[str]** |  | [optional] 
**keysign_ms** | **int** |  | [optional] 
**out_hashes** | **list[str]** |  | [optional] 
**status** | **str** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

