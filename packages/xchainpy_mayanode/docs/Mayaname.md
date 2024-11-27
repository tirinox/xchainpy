# Mayaname

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**expire_block_height** | **int** |  | [optional] 
**owner** | **str** |  | [optional] 
**preferred_asset** | **str** |  | 
**preferred_asset_swap_threshold_cacao** | **str** | Amount of CACAO currently required to swap to preferred asset (this is variable based on outbound fee of the asset). | [optional] 
**affiliate_collector_cacao** | **str** | Amount of CACAO currently accrued by this thorname in affiliate fees waiting to be swapped to preferred asset. | [optional] 
**aliases** | [**list[MayanameAlias]**](MayanameAlias.md) |  | 
**affiliate_bps** | **int** | Affiliate basis points for calculating affiliate fees, which are applied as the default basis points when the MAYAName is listed as an affiliate in swap memo. | [optional] 
**subaffiliates** | [**list[MayanameSubaffiliate]**](MayanameSubaffiliate.md) | List of subaffiliates and the corresponding affiliate basis points. If a MAYAName is specified as an affiliate in a swap memo, the shares of the affiliate fee are distributed among the listed subaffiliates based on the basis points assigned to each subaffiliate. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

