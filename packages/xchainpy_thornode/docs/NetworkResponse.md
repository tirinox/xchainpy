# NetworkResponse

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**bond_reward_rune** | **str** | total amount of RUNE awarded to node operators | 
**burned_bep_2_rune** | **str** | total of burned BEP2 RUNE | 
**burned_erc_20_rune** | **str** | total of burned ERC20 RUNE | 
**total_bond_units** | **str** | total bonded RUNE | 
**total_reserve** | **str** | total reserve RUNE | 
**vaults_migrating** | **bool** | Returns true if there exist RetiringVaults which have not finished migrating funds to new ActiveVaults | 
**gas_spent_rune** | **str** | Sum of the gas the network has spent to send outbounds | 
**gas_withheld_rune** | **str** | Sum of the gas withheld from users to cover outbound gas | 
**outbound_fee_multiplier** | **str** | Current outbound fee multiplier, in basis points | [optional] 
**outbound_tx_fee_rune** | **str** | the outbound transaction fee in rune, converted from the OutboundTransactionFeeUSD mimir | 
**native_tx_fee_rune** | **str** | the native transaction fee in rune, converted from the NativeTransactionFeeUSD mimir | 
**tns_register_fee_rune** | **str** | the thorname register fee in rune, converted from the TNSRegisterFeeUSD mimir | 
**tns_fee_per_block_rune** | **str** | the thorname fee per block in rune, converted from the TNSFeePerBlockUSD mimir | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

