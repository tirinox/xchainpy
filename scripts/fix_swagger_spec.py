"""
The current version of Swagger-codegen generates incomplete models for Python
when the root objects is array of $ref objects, e.g. `PoolsResponse` in the array of `Pool` objects.
So this scripts downloads the swagger spec, amends the models, and saves the result to a new file.

Dependencies:
    pip install pyyaml
"""

import argparse
import asyncio
import logging
import urllib.parse
from pprint import pprint

import yaml

from common import load_spec


def parse_args():
    parser = argparse.ArgumentParser(
        prog=__name__,
        description='Fix swagger spec',
    )
    parser.add_argument('-i', '--input', help='Input URL', required=True)
    parser.add_argument('-o', '--output', help='Output file')
    parser.add_argument('-m', '--mode', help='Script mode: MAYA, THOR', required=True)
    args = parser.parse_args()
    if not args.output:
        args.output = urllib.parse.urlparse(args.input).path.split('/')[-1]

    if args.mode.upper() not in ['MAYA', 'THOR', 'MIDGARD']:
        raise ValueError('Mode (-m mode) must be either MIDGARD, MAYA or THOR')

    print(f'Input: {args.input}')
    print(f'Output: {args.output}')
    return args


def drill(obj, path):
    if isinstance(path, str):
        components = path.split('.')
    else:
        components = path
    for c in components:
        obj = obj.get(c, {})
    return obj


def get_ref(r):
    ref = r.get('$ref')
    if ref:
        return ref, 'ref'
    ref = drill(r, 'content.application/json.schema.$ref')
    return ref, 'content'


def get_schema(spec, ref):
    components = ref.split('/')
    schema = spec
    for c in components:
        if c != '#':
            schema = schema.get(c, {})
    return schema


def is_simple_array(response_schema):
    if response_schema.get('type') == 'array':
        items_type = response_schema.get('items', {})
        if '$ref' in items_type:
            return items_type.get('$ref'), 'ref'
        else:
            return items_type, 'content'


def is_array(schema):
    return schema.get('type') == 'array'


def make_ref(ref):
    return {'$ref': ref}


def fix_spec(spec):
    """
    Fix the spec about array responses
    """
    paths = spec['paths']

    for path, method in paths.items():
        responses = drill(method, 'get.responses')
        if not responses:
            continue
        r200 = responses.get('200', {}) or responses.get(200, {})
        ref, ref_type = get_ref(r200)
        # e.g. : '#/components/schemas/LiquidityProviderResponse'
        if not ref:
            continue

        response_schema = get_schema(spec, ref)
        result = None

        ref2, ref_type2 = get_ref(response_schema)
        if ref2:
            print(f'Fixing simple ref {ref2}')

            # maybe go deeper?
            schema2 = get_schema(spec, ref2)
            if schema2:
                if is_array(schema2):
                    print(f'Detected simple array of {schema2}')
                    result = schema2.copy()
            if not result:
                result = make_ref(ref2)
        elif is_array(response_schema):
            print(f'Fixing simple array of {response_schema}')
            result = response_schema.copy()

        if result:
            r200.pop('$ref', None)
            if 'content' not in r200:
                r200['content'] = {
                    'application/json': {}
                }
            r200['content']['application/json']['schema'] = result

    return spec


def fix_maya_liquidity_providers(spec):
    place = drill(spec, ['paths', '/mayachain/pool/{asset}/liquidity_provider/{address}',
                         'get', 'responses', 200, 'content', 'application/json'])

    place['schema'] = {'$ref': '#/components/schemas/LiquidityProviderSummary'}

    return spec


def fix_thor_tx_details_nullable(spec):
    # nullable: true
    try:
        place = drill(spec, ['components', 'schemas', 'TxDetailsResponse', 'properties'])
        place['actions']['nullable'] = True
        place['out_txs']['nullable'] = True
    except Exception:
        logging.exception('Failed to fix TxDetailsResponse')
    return spec


def fix_thor_trade_account_array(spec):
    """
    /thorchain/trade/account/{address} should return an array of TradeAccountsResponse (arrau of objects)
    not just TradeAccountResponse which is a single object
    """
    place = drill(spec, ['paths', '/thorchain/trade/account/{address}',
                         'get', 'responses', 200, 'content', 'application/json'])
    place['schema'] = {'$ref': '#/components/schemas/TradeAccountsResponse'}

    place = drill(spec, ['components', 'schemas', 'TradeAccountsResponse'])
    place['items'] = {'$ref': '#/components/schemas/TradeAccountResponse'}  # instead of "items: *id021"

    return spec


def fix_thor_tx_required_gas_and_coins(spec):
    # nullable: true
    place = drill(spec, ['components', 'schemas', 'Tx', 'required'])
    prev = list(place)
    place.clear()
    print(f'Removed "gas" from required: {prev} -> {place}')
    return spec


def fix_thor_TxDetailsResponse_required(spec):
    # nullable: true
    place = drill(spec, ['components', 'schemas', 'TxDetailsResponse', 'required'])
    print(f'Cleared TxDetailsResponse required list: {place} -> []')
    place.clear()

    return spec


def add_readme(spec):
    spec['x-readme-file'] = 'README.md'
    return spec


async def main():
    args = parse_args()
    spec = await load_spec(args.input)

    print('Loaded spec:')
    pprint(spec, depth=2)

    print('Fixing spec...')

    # all modes

    # specific modes for different protocols
    if args.mode.upper() == 'MAYA':
        spec = fix_maya_liquidity_providers(spec)
    elif args.mode.upper() == 'THOR':
        spec = fix_thor_tx_details_nullable(spec)
        spec = fix_thor_trade_account_array(spec)
        spec = fix_thor_tx_required_gas_and_coins(spec)
        spec = fix_thor_TxDetailsResponse_required(spec)
    elif args.mode.upper() == 'MIDGARD':
        pass  # no specific fixes for Midgard yet

    spec = fix_spec(spec)
    spec = add_readme(spec)

    with open(args.output, 'w') as f:
        yaml.dump(spec, f, sort_keys=False)
    print(f'Saved to {args.output}')


if __name__ == '__main__':
    asyncio.run(main())
