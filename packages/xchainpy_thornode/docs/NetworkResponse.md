# NetworkResponse

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**bond_reward_rune** | **str** | total amount of RUNE awarded to node operators | 
**total_bond_units** | **str** | total bonded RUNE | 
**effective_security_bond** | **str** | effective security bond used to determine maximum pooled RUNE | 
**total_reserve** | **str** | total reserve RUNE | 
**vaults_migrating** | **bool** | Returns true if there exist RetiringVaults which have not finished migrating funds to new ActiveVaults | 
**gas_spent_rune** | **str** | Sum of the gas the network has spent to send outbounds | 
**gas_withheld_rune** | **str** | Sum of the gas withheld from users to cover outbound gas | 
**outbound_fee_multiplier** | **str** | Current outbound fee multiplier, in basis points | [optional] 
**native_outbound_fee_rune** | **str** | the outbound transaction fee in rune, converted from the NativeOutboundFeeUSD mimir (after USD fees are enabled) | 
**native_tx_fee_rune** | **str** | the native transaction fee in rune, converted from the NativeTransactionFeeUSD mimir (after USD fees are enabled) | 
**tns_register_fee_rune** | **str** | the thorname register fee in rune, converted from the TNSRegisterFeeUSD mimir (after USD fees are enabled) | 
**tns_fee_per_block_rune** | **str** | the thorname fee per block in rune, converted from the TNSFeePerBlockUSD mimir (after USD fees are enabled) | 
**rune_price_in_tor** | **str** | the rune price in tor | 
**tor_price_in_rune** | **str** | the tor price in rune | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

