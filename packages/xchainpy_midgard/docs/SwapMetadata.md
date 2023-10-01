# SwapMetadata

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**affiliate_address** | **str** | Affiliate fee address of the swap, empty if fee swap | 
**affiliate_fee** | **str** | Int64 (Basis points, 0-1000, where 1000&#x3D;10%) | 
**is_streaming_swap** | **bool** | indicate whether this action was streaming | 
**liquidity_fee** | **str** | Int64(e8), RUNE amount charged as swap liquidity fee | 
**memo** | **str** | Transaction memo of the swap action | 
**network_fees** | [**NetworkFees**](NetworkFees.md) |  | 
**streaming_swap_meta** | [**StreamingSwapMeta**](StreamingSwapMeta.md) |  | [optional] 
**swap_slip** | **str** | Int64 (Basis points, 0-10000, where 10000&#x3D;100%), swap slip percentage | 
**swap_target** | **str** | Int64(e8), minimum output amount specified for the swap | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

