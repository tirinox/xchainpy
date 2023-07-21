.PHONY: dev_tools cli_codegen test

dev_tools:
	pip install -U pytest pytest-asyncio requests-mock aioresponses

cli_codegen:
	cd scripts && \
		./gen_thornode_client.sh \
		./gen_midgard_client.sh \
		./gen_mayanode_client.sh


test:
	pytest \
		packages/xchainpy_client \
		packages/xchainpy_cosmos \
		packages/xchainpy_crypto \
		packages/xchainpy_thorchain \
		packages/xchainpy_thorchain_amm \
		packages/xchainpy_thorchain_query \
		packages/xchainpy_util
