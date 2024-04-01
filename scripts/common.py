import json
import sys

import yaml
from aiohttp import ClientSession


def extract_version(spec):
    return spec.get('info', {}).get('version')


async def fetch(url):
    async with ClientSession() as session:
        user_agent = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 OPR/72.0.3815.465 (Edition Yx GX)',
        }
        async with session.get(url, headers=user_agent) as response:
            return await response.text()


async def load_spec(input_file):
    input_data = await fetch(input_file)
    try:
        spec = json.loads(input_data)
    except json.decoder.JSONDecodeError as e:
        try:
            spec = yaml.load(input_data, Loader=yaml.FullLoader)
        except Exception as e:
            print(f'Failed to load YAML: {e}')
            sys.exit(2)
    return spec
