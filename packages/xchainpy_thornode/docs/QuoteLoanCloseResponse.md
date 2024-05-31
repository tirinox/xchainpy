# QuoteLoanCloseResponse

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
**recommended_gas_rate** | **str** | the recommended gas rate to use for the inbound to ensure timely confirmation | [optional] 
**gas_rate_units** | **str** | the units of the recommended gas rate | [optional] 
**memo** | **str** | generated memo for the loan close | 
**expected_amount_out** | **str** | the amount of collateral asset the user can expect to receive after fees in 1e8 decimals | 
**expected_amount_in** | **str** | The quantity of the repayment asset to be sent by the user, calculated as the desired percentage of the loan&#x27;s value, expressed in units of 1e8 | 
**expected_collateral_withdrawn** | **str** | the expected amount of collateral decrease on the loan | 
**expected_debt_repaid** | **str** | the expected amount of TOR debt decrease on the loan | 
**streaming_swap_blocks** | **int** | The number of blocks involved in the streaming swaps during the repayment process. | 
**streaming_swap_seconds** | **int** | The approximate number of seconds taken by the streaming swaps involved in the repayment process. | 
**total_repay_seconds** | **int** | The total expected duration for a repayment, measured in seconds, which includes the time for inbound confirmation, the duration of streaming swaps, and any outbound delays. | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

