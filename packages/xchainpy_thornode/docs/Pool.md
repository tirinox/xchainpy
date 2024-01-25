# Pool

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asset** | **str** |  | 
**short_code** | **str** |  | [optional] 
**status** | **str** |  | 
**decimals** | **int** |  | [optional] 
**pending_inbound_asset** | **str** |  | 
**pending_inbound_rune** | **str** |  | 
**balance_asset** | **str** |  | 
**balance_rune** | **str** |  | 
**pool_units** | **str** | the total pool units, this is the sum of LP and synth units | 
**lp_units** | **str** | the total pool liquidity provider units | 
**synth_units** | **str** | the total synth units in the pool | 
**synth_supply** | **str** | the total supply of synths for the asset | 
**savers_depth** | **str** | the balance of L1 asset deposited into the Savers Vault | 
**savers_units** | **str** | the number of units owned by Savers | 
**synth_mint_paused** | **bool** | whether additional synths cannot be minted | 
**synth_supply_remaining** | **str** | the amount of synth supply remaining before the current max supply is reached | 
**loan_collateral** | **str** | the amount of collateral collects for loans | 
**loan_collateral_remaining** | **str** | the amount of remaining collateral collects for loans | 
**loan_cr** | **str** | the current loan collateralization ratio | 
**derived_depth_bps** | **str** | the depth of the derived virtual pool relative to L1 pool (in basis points) | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

