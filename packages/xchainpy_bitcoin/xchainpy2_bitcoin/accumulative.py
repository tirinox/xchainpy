# Baseline estimates, used to improve performance
import math

TX_EMPTY_SIZE = 4 + 1 + 1 + 4
TX_INPUT_BASE = 32 + 4 + 1 + 4
TX_INPUT_PUBKEYHASH = 107
TX_OUTPUT_BASE = 8 + 1
TX_OUTPUT_PUBKEYHASH = 25


class AccumulativeResult:
    def __init__(self, fee=-1, inputs=None, outputs=None):
        self.fee = fee
        self.inputs = inputs
        self.outputs = outputs

    def __getitem__(self, key):
        return getattr(self, key)

    def input_value(self, index):
        return get_value(self.inputs[index])

    def output_value(self, index):
        return get_value(self.outputs[index])

    def __repr__(self):
        return f"AccumulativeResult(fee={self.fee}, inputs={self.inputs}, outputs={self.outputs})"


def script_length(item):
    if isinstance(item, (str, bytes)):
        return len(item)
    elif isinstance(item, dict) and 'length' in item:
        return int(item['length'])
    else:
        return 0


def get_script(item):
    if isinstance(item, dict):
        return item.get('script')
    else:
        return None


def input_bytes(_input):
    if isinstance(_input, int):
        return TX_INPUT_BASE + TX_INPUT_PUBKEYHASH
    return TX_INPUT_BASE + (script_length(script) if (script := get_script(_input)) else TX_INPUT_PUBKEYHASH)


def output_bytes(output):
    if isinstance(output, int):
        return TX_OUTPUT_BASE + TX_OUTPUT_PUBKEYHASH
    return TX_OUTPUT_BASE + (script_length(script) if (script := get_script(output)) else TX_OUTPUT_PUBKEYHASH)


def dust_threshold(fee_rate):
    # ... classify the output for input estimate
    return input_bytes({}) * fee_rate


def transaction_bytes(inputs, outputs):
    return (
            TX_EMPTY_SIZE
            + sum(input_bytes(x) for x in inputs)
            + sum(output_bytes(x) for x in outputs)
    )


def uint_or_nan(v):
    nan = float('nan')
    if not isinstance(v, (int, float)):
        return nan
    if not is_finite(v):
        return nan
    if int(v) != v:
        return nan
    if v < 0:
        return nan
    return v


def get_value(v):
    if isinstance(v, (int, float)):
        return v
    else:
        return v.get('value')


def sum_forgiving(_range):
    return sum(get_value(x) if is_finite(get_value(x)) else 0 for x in _range)


def sum_or_nan(_range):
    return sum(uint_or_nan(get_value(x)) for x in _range)


BLANK_OUTPUT = output_bytes({})


def finalize(inputs, outputs, fee_rate):
    bytes_accum = transaction_bytes(inputs, outputs)
    fee_after_extra_output = fee_rate * (bytes_accum + BLANK_OUTPUT)
    remainder_after_extra_output = sum_or_nan(inputs) - (sum_or_nan(outputs) + fee_after_extra_output)

    # is it worth a change output?
    if remainder_after_extra_output > dust_threshold(fee_rate):
        outputs.append({'value': remainder_after_extra_output})

    fee = sum_or_nan(inputs) - sum_or_nan(outputs)
    if not is_finite(fee):
        return AccumulativeResult(fee_rate * bytes_accum)

    return AccumulativeResult(fee, inputs, outputs)


def is_finite(v):
    return isinstance(v, (int, float)) and math.isfinite(v)


def accumulative(utxos, outputs, fee_rate):
    if not is_finite(uint_or_nan(fee_rate)):
        return AccumulativeResult(-1)

    bytes_accum = transaction_bytes([], outputs)
    in_accum = 0
    inputs = []
    out_accum = sum_or_nan(outputs)

    for i in range(len(utxos)):
        utxo = utxos[i]
        utxo_bytes = input_bytes(utxo)
        utxo_fee = fee_rate * utxo_bytes
        # utxo_value = uint_or_nan(utxo['value'])
        utxo_value = uint_or_nan(get_value(utxo))

        # skip detrimental input
        if utxo_fee > utxo_value:
            if i == len(utxos) - 1:
                return AccumulativeResult(fee_rate * (bytes_accum + utxo_bytes))
            continue

        bytes_accum += utxo_bytes
        in_accum += utxo_value
        inputs.append(utxo)

        fee = fee_rate * bytes_accum

        # go again?
        if in_accum < out_accum + fee:
            continue

        return finalize(inputs, outputs, fee_rate)

    return AccumulativeResult(fee_rate * bytes_accum)
