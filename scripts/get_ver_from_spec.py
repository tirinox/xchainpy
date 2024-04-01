import asyncio
import sys
from common import load_spec, extract_version


async def main():
    if len(sys.argv) != 2:
        print('Usage: get_ver_from_spec.py <path-to-spec>')
        sys.exit(1)

    input_file = sys.argv[1]
    spec = await load_spec(input_file)
    if not spec:
        print('Failed to load spec')
        sys.exit(1)

    version = extract_version(spec)
    print(version)


if __name__ == '__main__':
    asyncio.run(main())
