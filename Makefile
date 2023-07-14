.PHONY: dev_tools cli_codegen

dev_tools:
	pip install -U pytest pytest-asyncio

cli_codegen:
	cd scripts
	./gen_thornode_client.sh
	./gen_midgard_client.sh
	./gen_mayanode_client.sh