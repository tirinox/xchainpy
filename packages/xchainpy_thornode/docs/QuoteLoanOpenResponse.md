# QuoteLoanOpenResponse

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**inbound_address** | **str** | the inbound address for the transaction on the source chain | [optional] 
**inbound_confirmation_blocks** | **int** | the approximate number of source chain blocks required before processing | [optional] 
**inbound_confirmation_seconds** | **int** | the approximate seconds for block confirmations required before processing | [optional] 
**outbound_delay_blocks** | **int** | the number of thorchain blocks the outbound will be delayed | 
**outbound_delay_seconds** | **int** | the approximate seconds for the outbound delay before it will be sent | 
**fees** | [**QuoteFees**](QuoteFees.md) |  | 
**slippage_bps** | **int** | Deprecated - migrate to fees object. | [optional] 
**streaming_slippage_bps** | **int** | Deprecated - migrate to fees object. | [optional] 
**router** | **str** | the EVM chain router contract address | [optional] 
**expiry** | **int** | expiration timestamp in unix seconds | 
**warning** | **str** | static warning message | 
**notes** | **str** | chain specific quote notes | 
**dust_threshold** | **str** | Defines the minimum transaction size for the chain in base units (sats, wei, uatom). Transactions with asset amounts lower than the dust_threshold are ignored. | [optional] 
**recommended_min_amount_in** | **str** | The recommended minimum inbound amount for this transaction type &amp; inbound asset. Sending less than this amount could result in failed refunds. | [optional] 
**memo** | **str** | generated memo for the loan open | [optional] 
**expected_amount_out** | **str** | the amount of the target asset the user can expect to receive after fees in 1e8 decimals | 
**expected_collateralization_ratio** | **str** | the expected collateralization ratio in basis points | 
**expected_collateral_deposited** | **str** | the expected amount of collateral increase on the loan | 
**expected_debt_issued** | **str** | the expected amount of TOR debt increase on the loan | 
**streaming_swap_blocks** | **int** | The number of blocks involved in the streaming swaps during the open loan process. | 
**streaming_swap_seconds** | **int** | The approximate number of seconds taken by the streaming swaps involved in the open loan process. | 
**total_open_loan_seconds** | **int** | The total expected duration for a open loan, measured in seconds, which includes the time for inbound confirmation, the duration of streaming swaps, and any outbound delays. | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

