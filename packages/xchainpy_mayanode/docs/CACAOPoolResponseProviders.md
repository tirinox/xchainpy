# CACAOPoolResponseProviders

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**units** | **str** | the units of CACAOPool owned by providers (including pending) | 
**pending_units** | **str** | the units of CACAOPool owned by providers that remain pending | 
**pending_cacao** | **str** | the amount of CACAO pending | 
**value** | **str** | the value of the provider share of the CACAOPool (includes pending CACAO) | 
**pnl** | **str** | the profit and loss of the provider share of the CACAOPool | 
**current_deposit** | **str** | the current CACAO deposited by providers | 
**total_units** | **str** | total units in the CACAOPool (PoolUnits + ReserveUnits) | 
**pool_value** | **str** | total CACAO held by the CACAOPool module | 
**member_deposit** | **str** | aggregate net deposits by providers (sum of deposit_amount - withdraw_amount per member) | 
**real_pnl** | **str** | aggregate PnL computed from individual members (sum of value - deposit_amount + withdraw_amount per member) | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

