UV ?= uv

default: help

.PHONY: help
help: # Show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 -_]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

.PHONY: dev_tools
dev_tools: # Install dev tools
	$(UV) sync --group dev

.PHONY: gen_thornode
gen_thornode: # Generate thornode client from OpenAPI spec
	cd scripts && ./gen_thornode_client.sh

.PHONY: gen_mayanode
gen_mayanode: # Generate mayanode client from OpenAPI spec
	cd scripts && ./gen_mayanode_client.sh

.PHONY: gen_midgard
gen_midgard: # Generate midgard client of THORChain protocol from OpenAPI spec
	cd scripts && ./gen_midgard_client.sh

.PHONY: gen_midgard_maya
gen_midgard_maya: # Generate Midgard client of MayaProtocol from OpenAPI spec
	cd scripts && ./gen_midgard_client_maya.sh

.PHONY: test
test: # Run tests
	$(UV) run pytest \
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
		packages/xchainpy_base \
		packages/xchainpy_wallet

.PHONY: tc_env
tc_env: # Install XChainPy2 packages in editable mode
	$(UV) sync --all-packages --group dev

.PHONY: install_editable
install_editable: # Install XChainPy2's any single package in editable mode
	cd scripts && UV=$(UV) ./install_editable.sh

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
	cd docs && $(UV) run --project .. make html && open _build/html/index.html

.PHONY: upver
upver: # Helper script to raise package version number, you will be asked which package to update
	cd scripts && ./upver.sh

.PHONY: versions
versions: # Show versions of all packages
	cd scripts && python print_version_vs_pypi.py
