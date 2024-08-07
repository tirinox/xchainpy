# InboundAddress

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**chain** | **str** |  | [optional] 
**pub_key** | **str** |  | [optional] 
**address** | **str** |  | [optional] 
**router** | **str** |  | [optional] 
**halted** | **bool** |  | 
**global_trading_paused** | **bool** | Returns true if trading is paused globally | [optional] 
**chain_trading_paused** | **bool** | Returns true if trading is paused for this chain | [optional] 
**chain_lp_actions_paused** | **bool** | Returns true if LP actions are paused for this chain | [optional] 
**gas_rate** | **str** | The minimum fee rate used by vaults to send outbound TXs. The actual fee rate may be higher. For EVM chains this is returned in gwei (1e9). | [optional] 
**gas_rate_units** | **str** | Units of the gas_rate. | [optional] 
**outbound_tx_size** | **str** | Avg size of outbound TXs on each chain. For UTXO chains it may be larger than average, as it takes into account vault consolidation txs, which can have many vouts | [optional] 
**outbound_fee** | **str** | The total outbound fee charged to the user for outbound txs in the gas asset of the chain. | [optional] 
**dust_threshold** | **str** | Defines the minimum transaction size for the chain in base units (sats, wei, uatom). Transactions with asset amounts lower than the dust_threshold are ignored. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

