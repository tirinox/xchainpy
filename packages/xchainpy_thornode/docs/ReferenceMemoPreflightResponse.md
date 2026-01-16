# ReferenceMemoPreflightResponse

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**reference** | **str** | the reference ID that would be generated from the amount | 
**available** | **bool** | whether this reference is currently available (not registered or expired) | 
**can_register** | **bool** | whether a new registration can be made with this reference | 
**expires_at** | **str** | block height when current registration expires (0 if available) | 
**memo** | **str** | the currently registered memo (only present if not available) | [optional] 
**usage_count** | **str** | the number of times this reference has been used | 
**max_use** | **str** | the maximum number of times this reference can be used (0 &#x3D; unlimited) | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

