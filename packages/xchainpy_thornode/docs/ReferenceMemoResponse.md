# ReferenceMemoResponse

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asset** | **str** | the asset for which this reference memo is valid | 
**memo** | **str** | the original memo that was registered for memoless transactions | 
**reference** | **str** | the reference number used to identify this memo | 
**height** | **str** | the block height when this reference memo was registered | 
**registration_hash** | **str** | the transaction hash where this reference memo was registered | 
**registered_by** | **str** | the address that registered this reference memo | 
**used_by_txs** | **list[str]** | list of transaction hashes that have used this reference memo | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

