"""
The current version of Swagger-codegen generates incomplete models for Python
when the root objects is array of $ref objects, e.g. `PoolsResponse` in the array of `Pool` objects.
So this scripts downloads the swagger spec, amends the models, and saves the result to a new file.

Dependencies:
    pip install pyyaml
"""

import argparse
import json
import urllib.parse
from pprint import pprint
from urllib.request import urlopen

import yaml


def parse_args():
    parser = argparse.ArgumentParser(
        prog=__name__,
        description='Fix swagger spec',
    )
    parser.add_argument('-i', '--input', help='Input URL', required=True)
    parser.add_argument('-o', '--output', help='Output file')
    args = parser.parse_args()
    if not args.output:
        args.output = urllib.parse.urlparse(args.input).path.split('/')[-1]

    print(f'Input: {args.input}')
    print(f'Output: {args.output}')
    return args


def drill(obj, path):
    components = path.split('.')
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
                    result = schema2
            if not result:
                result = make_ref(ref2)
        elif is_array(response_schema):
            print(f'Fixing simple array of {response_schema}')
            result = response_schema

        if result:
            r200.pop('$ref', None)
            if 'content' not in r200:
                r200['content'] = {
                    'application/json': {}
                }
            r200['content']['application/json']['schema'] = result

        """ 
  THORNode:
    LiquidityProviderResponse:
      $ref: '#/components/schemas/LiquidityProvider'
    SaverResponse:
      $ref: '#/components/schemas/Saver'
    SaversResponse:
      type: array
      items:
        $ref: '#/components/schemas/Saver'
----------------------------------------------------
 Midgard:
    EarningsHistoryResponse:
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/EarningsHistory'
    """

    return spec


def fix_array(mount_point, path, item_type):
    print(f'Fixing {path}...')


def main():
    args = parse_args()
    input_data = urlopen(args.input).read().decode('utf-8')
    try:
        spec = json.loads(input_data)
    except json.decoder.JSONDecodeError as e:
        print('Input is not a valid JSON, perhaps it is YAML?')
        spec = yaml.load(input_data, Loader=yaml.FullLoader)
    print('Loaded spec:')
    pprint(spec, depth=2)

    print('Fixing spec...')
    spec = fix_spec(spec)

    with open(args.output, 'w') as f:
        yaml.dump(spec, f, sort_keys=False)
    print(f'Saved to {args.output}')


if __name__ == '__main__':
    main()
