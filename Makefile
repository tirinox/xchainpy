.PHONY: dev_tools test tc_env build publish_test publish gen_thornode gen_mayanode gen_midgard gen_binance_proto

dev_tools:
	pip install -U pytest pytest-asyncio requests-mock aioresponses

gen_thornode:
	cd scripts && ./gen_thornode_client.sh

gen_mayanode:
	cd scripts && ./gen_mayanode_client.sh

gen_midgard:
	cd scripts && ./gen_midgard_client.sh


gen_binance_proto:
	cd scripts && ./gen_proto_binance_chain.sh


test:
	pytest \
		packages/xchainpy_client \
		packages/xchainpy_cosmos \
		packages/xchainpy_crypto \
		packages/xchainpy_thorchain \
		packages/xchainpy_thorchain_amm \
		packages/xchainpy_thorchain_query \
		packages/xchainpy_utils \
		packages/xchainpy_bitcoin \
		packages/xchainpy_mayachain \
		packages/xchainpy_litecoin \
		packages/xchainpy_bsc \
		packages/xchainpy_dogecoin \
		packages/xchainpy_avalanche


tc_env:
	python3 -m pip install --editable packages/xchainpy_crypto
	python3 -m pip install --editable packages/xchainpy_utils
	python3 -m pip install --editable packages/xchainpy_client
	python3 -m pip install --editable packages/xchainpy_cosmos
	python3 -m pip install --editable packages/xchainpy_thorchain
	python3 -m pip install --editable packages/xchainpy_bitcoin
	python3 -m pip install --editable packages/xchainpy_litecoin
	python3 -m pip install --editable packages/xchainpy_dogecoin
	python3 -m pip install --editable packages/xchainpy_bitcoincash
	python3 -m pip install --editable packages/xchainpy_binance
	python3 -m pip install --editable packages/xchainpy_ethereum
	python3 -m pip install --editable packages/xchainpy_bsc
	python3 -m pip install --editable packages/xchainpy_avalanche


build:
	cd scripts && ./publish.sh build

publish_test:
	cd scripts && ./publish.sh publish_test

publish:
	cd scripts && ./publish.sh publish
