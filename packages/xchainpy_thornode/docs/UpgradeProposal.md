# UpgradeProposal

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | the name of the upgrade | 
**height** | **int** | the block height at which the upgrade will occur | 
**info** | **str** | the description of the upgrade, typically json with URLs to binaries for use with automation tools | 
**approved** | **bool** | whether the upgrade has been approved by the active validators | [optional] 
**approved_percent** | **str** | the percentage of active validators that have approved the upgrade | [optional] 
**validators_to_quorum** | **int** | the amount of additional active validators required to reach quorum for the upgrade | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

