# OutboundFee

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asset** | **str** | the asset to display the outbound fee for | 
**outbound_fee** | **str** | the asset&#x27;s outbound fee, in (1e8-format) units of the asset | 
**fee_withheld_rune** | **str** | Total RUNE the network has withheld as fees to later cover gas costs for this asset&#x27;s outbounds | [optional] 
**fee_spent_rune** | **str** | Total RUNE the network has spent to reimburse gas costs for this asset&#x27;s outbounds | [optional] 
**surplus_rune** | **str** | amount of RUNE by which the fee_withheld_rune exceeds the fee_spent_rune | [optional] 
**dynamic_multiplier_basis_points** | **str** | dynamic multiplier basis points, based on the surplus_rune, affecting the size of the outbound_fee | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

