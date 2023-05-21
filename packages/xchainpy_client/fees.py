from packages.xchainpy_client.models import FeeType, Fee, Fees, FeeOption


def single_fee(fee_type: FeeType, amount: Fee) -> Fees:
    return Fees(
        type=fee_type,
        fees={
            option: amount for option in FeeOption
        }
    )


def standart_fee(fee_type: FeeType, amount: Fee) -> Fees:
    fees = single_fee(fee_type, amount)
    fees.fees[FeeOption.AVERAGE] = amount * 0.5
    fees.fees[FeeOption.FASTEST] = amount * 5
    return fees