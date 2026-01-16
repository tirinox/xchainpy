# TxSignersResponse

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tx_id** | **str** |  | [optional] 
**tx** | [**ObservedTx**](ObservedTx.md) |  | 
**txs** | [**list[ObservedTx]**](ObservedTx.md) |  | 
**actions** | [**list[TxOutItem]**](TxOutItem.md) |  | 
**out_txs** | [**list[Tx]**](Tx.md) |  | 
**consensus_height** | **int** | the mayachain height at which the inbound reached consensus | [optional] 
**finalised_height** | **int** | the mayachain height at which the outbound was finalised | [optional] 
**updated_vault** | **bool** |  | [optional] 
**reverted** | **bool** |  | [optional] 
**outbound_height** | **int** | the mayachain height for which the outbound was scheduled | [optional] 
**refund_height** | **int** | the mayachain height at which a refund was scheduled/emitted | [optional] 
**refunded_amount** | **str** | the amount refunded to the inbound source | [optional] 
**partial_refund** | **bool** |  | [optional] 
**refund_reason** | **str** | the reason for the failure of the most recent streaming swap attempt, which resulted in a refund | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

