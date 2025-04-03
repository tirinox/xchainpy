# Network

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**active_bonds** | **list[str]** | Array of rune amounts (e8) bonded by each active node.  | 
**active_node_count** | **str** | Int64, Number of active nodes | 
**block_rewards** | [**BlockRewards**](BlockRewards.md) |  | 
**bond_metrics** | [**BondMetrics**](BondMetrics.md) |  | 
**bonding_apy** | **str** | Float, E.g. 0.01 &#x3D; 1%. Estimate of the compounded bonding earnings based on the current reserve size, emmission curve, blocks per year and pool share factor &#x3D; (WeeklyBondIncome/BondAmount + 1)^52 - 1  | 
**liquidity_apy** | **str** | Float, E.g. 0.01 &#x3D; 1%. Estimate of the compounded  liquidity provider earnings based on the current reserve size, emmission curve, blocks per year and pool share factor &#x3D; (WeeklyLiquidityIncome/(totalPooledRune*2) + 1)^52 - 1  | 
**next_churn_height** | **str** | Int64, height (block number) of the next churn. | 
**pool_activation_countdown** | **str** | Int64, the remaining time of pool activation (in blocks) | 
**pool_share_factor** | **str** | Float [0..1], the ratio which is used to split earnings between liquidity provider and nodes. LPIncome &#x3D; rewards * poolShareFactor ; BondIncome :&#x3D;  rewards * (1 - poolShareFactor)  | 
**standby_bonds** | **list[str]** | Array of rune amounts (e8) bonded by each standby node.  | 
**standby_node_count** | **str** | Int64, Number of standby nodes, some of them might become active at the next churn.  | 
**total_pooled_rune** | **str** | Int64(e8), total Rune in all pools. Because asset and Rune value is the same amount in every pool (by definition), the total amount pooled is totalPooledRune*2.  | 
**total_reserve** | **str** | Int64(e8), Current size of the Reserve. | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

