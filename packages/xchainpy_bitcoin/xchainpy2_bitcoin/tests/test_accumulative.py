# load the test data
import json
import os.path

import pytest

from xchainpy2_bitcoin.accumulative import accumulative, AccumulativeResult

with open(os.path.join(os.path.dirname(__file__), 'accumulative_test_data.json')) as f:
    FIXTURES = json.load(f)


@pytest.mark.parametrize('case', FIXTURES)
def test_accumulative(case):
    inputs = case['inputs']
    outputs = case['outputs']
    fee_rate = case['feeRate']
    expected = case['expected']

    result = accumulative(inputs, outputs, fee_rate)
    expected = AccumulativeResult(**expected)
    assert result.fee == expected.fee

    assert (not result.inputs and not expected.inputs) or (len(result.inputs) == len(expected.inputs))
    assert (not result.outputs and not expected.outputs) or (len(result.outputs) == len(expected.outputs))

    if result.inputs and expected.inputs:
        for i in range(len(result.inputs)):
            assert result.input_value(i) == expected.input_value(i)
    if result.outputs and expected.outputs:
        for i in range(len(result.outputs)):
            assert result.output_value(i) == expected.output_value(i)


"""
var coinAccum = require('../accumulative')
var fixtures = require('./fixtures/accumulative')
var tape = require('tape')
var utils = require('./_utils')

fixtures.forEach(function (f) {
  tape(f.description, function (t) {
    var inputs = utils.expand(f.inputs, true)
    var outputs = utils.expand(f.outputs)
    var actual = coinAccum(inputs, outputs, f.feeRate)

    t.same(actual, f.expected)
    if (actual.inputs) {
      var feedback = coinAccum(actual.inputs, actual.outputs, f.feeRate)
      t.same(feedback, f.expected)
    }

    t.end()
  })
})
"""
