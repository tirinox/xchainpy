# TxDetailsResponse

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tx_id** | **str** |  | [optional] 
**tx** | [**ObservedTx**](ObservedTx.md) |  | 
**txs** | [**list[ObservedTx]**](ObservedTx.md) |  | 
**actions** | [**list[TxOutItem]**](TxOutItem.md) |  | 
**out_txs** | [**list[Tx]**](Tx.md) |  | 
**consensus_height** | **int** | the thorchain height at which the inbound reached consensus | [optional] 
**finalised_height** | **int** | the thorchain height at which the outbound was finalised | [optional] 
**updated_vault** | **bool** |  | [optional] 
**reverted** | **bool** |  | [optional] 
**outbound_height** | **int** | the thorchain height for which the outbound was scheduled | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

