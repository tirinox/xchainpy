# RefundMetadata

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**affiliate_address** | **str** | Affiliate fee address of the swap, empty if fee swap | 
**affiliate_fee** | **str** | Int64 (Basis points, 0-1000, where 1000&#x3D;10%) | 
**memo** | **str** | Transaction memo of the refund action | 
**network_fees** | [**NetworkFees**](NetworkFees.md) |  | 
**reason** | **str** | Reason for the refund | 
**tx_type** | **str** | The type of the transaction given from its Memo Type of Transaction type:  \&quot;unknown\&quot;, \&quot;add\&quot;, \&quot;withdraw\&quot;, \&quot;swap\&quot;, \&quot;limitOrder\&quot;, \&quot;outbound\&quot;, \&quot;donate\&quot;, \&quot;bond\&quot;, \&quot;unbond\&quot;, \&quot;leave\&quot;, \&quot;yggdrasilFund\&quot;, \&quot;yggdrasilReturn\&quot;, \&quot;reserve\&quot;, \&quot;refund\&quot;, \&quot;migrate\&quot;, \&quot;ragnarok\&quot;, \&quot;switch\&quot;, \&quot;noOp\&quot;, \&quot;consolidate\&quot;, \&quot;thorname\&quot;, \&quot;loanOpen\&quot;, \&quot;loanRepayment\&quot;  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

