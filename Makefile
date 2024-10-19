default: help

.PHONY: help
help: # Show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 -_]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

.PHONY: dev_tools
dev_tools: # Install dev tools
	#pip install -U pytest pytest-asyncio requests-mock aioresponses sphinx sphinx-rtd-theme
	pip install -r requirements.txt

.PHONY: gen_thornode
gen_thornode: # Generate thornode client from OpenAPI spec
	cd scripts && ./gen_thornode_client.sh

.PHONY: gen_mayanode
gen_mayanode: # Generate mayanode client from OpenAPI spec
	cd scripts && ./gen_mayanode_client.sh

.PHONY: gen_midgard
gen_midgard: # Generate midgard client from OpenAPI spec
	cd scripts && ./gen_midgard_client.sh

.PHONY: gen_binance_proto
gen_binance_proto: # Generate Binance chain proto files
	cd scripts && ./gen_proto_binance_chain.sh

.PHONY: test
test: # Run tests
	pytest \
		packages/xchainpy_client \
		packages/xchainpy_cosmos \
		packages/xchainpy_crypto \
		packages/xchainpy_thorchain \
		packages/xchainpy_thorchain_amm \
		packages/xchainpy_thorchain_query \
		packages/xchainpy_utils \
		packages/xchainpy_bitcoin \
		packages/xchainpy_bitcoincash \
		packages/xchainpy_dogecoin \
		packages/xchainpy_litecoin \
		packages/xchainpy_mayachain \
		packages/xchainpy_bsc \
		packages/xchainpy_avalanche \
		packages/xchainpy_arbitrum \
		packages/xchainpy_wallet

.PHONY: tc_env
tc_env: # Install XChainPy2 packages in editable mode
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
	python3 -m pip install --editable packages/xchainpy_arbitrum
	python3 -m pip install --editable packages/xchainpy_wallet

.PHONY: build
build: # Build packages (without publishing)
	cd scripts && ./publish.sh build

.PHONY: publish_test
publish_test: # Publish packages to test pypi. You will be asked which package to publish
	cd scripts && ./publish.sh publish_test

.PHONY: publish
publish: # Publish packages to pypi. You will be asked which package to publish
	cd scripts && ./publish.sh publish

.PHONY: doc
doc: # Build documentation
	cd docs && make html && open _build/html/index.html

.PHONY: upver
upver: # Helper script to raise package version number, you will be asked which package to update
	cd scripts && ./upver.sh
