# Node

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**node_address** | **str** |  | 
**status** | **str** |  | 
**pub_key_set** | [**NodePubKeySet**](NodePubKeySet.md) |  | 
**aztec_address** | **str** |  | 
**validator_cons_pub_key** | **str** | the consensus pub key for the node | 
**peer_id** | **str** | the P2PID (:6040/p2pid endpoint) of the node | 
**bond** | **str** | current node bond | 
**reward** | **str** |  | 
**active_block_height** | **int** | the block height at which the node became active | 
**bond_address** | **str** |  | 
**status_since** | **int** | the block height of the current provided information for the node | 
**signer_membership** | **list[str]** | the set of vault public keys of which the node is a member | 
**requested_to_leave** | **bool** |  | 
**forced_to_leave** | **bool** | indicates whether the node has been forced to leave by the network, typically via ban | 
**leave_height** | **int** |  | 
**ip_address** | **str** |  | 
**version** | **str** | the currently set version of the node | 
**slash_points** | **int** | the accumulated slash points, reset at churn but excessive slash points may carry over | 
**jail** | [**NodeJail**](NodeJail.md) |  | 
**observe_chains** | [**list[ChainHeight]**](ChainHeight.md) | the last observed heights for all chain by the node | 
**preflight_status** | [**NodePreflightStatus**](NodePreflightStatus.md) |  | 
**bond_providers** | [**NodeBondProviders**](NodeBondProviders.md) |  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

