# AGENTS.md

## Scope and intent
- This repo is a multi-package Python workspace (`packages/xchainpy_*`) implementing a shared cross-chain client interface plus THORChain/Maya higher-level query + AMM flows.
- Prefer minimal, package-scoped edits: each package is publishable on its own and wired together via editable installs.

## Architecture at a glance
- Core abstraction is `XChainClient` in `packages/xchainpy_client/xchainpy2_client/base_client.py` (address/key mgmt, transfer/query contract, explorer URLs, async helpers).
- Chain clients extend that base by family:
  - Cosmos-style: `CosmosGaiaClient` -> `THORChainClient` / `MayaChainClient` (`packages/xchainpy_cosmos/...`, `packages/xchainpy_thorchain/...`).
  - EVM-style: `EthereumClient` -> `BinanceSmartChainClient` / `AvalancheClient` / `ArbitrumClient`.
  - UTXO-style: `BitcoinClient` reused by LTC/DOGE; BCH has its own client.
- `THORChainQuery` + `THORChainCache` (`packages/xchainpy_thorchain_query/...`) form the read/estimation layer over Midgard + THORNode/MayaNode with retry, backup hosts, and TTL caches.
- `Wallet` (`packages/xchainpy_wallet/xchainpy2_wallet/wallet.py`) composes installed chain clients; `detect_clients.py` maps `Chain -> Client` and intentionally degrades missing deps to `NoClient`.
- `THORChainAMM` (`packages/xchainpy_thorchain_amm/xchainpy2_thorchain_amm/amm.py`) is orchestration: quote via query layer, then deposit/transfer via chain clients.

## Generated vs hand-written boundaries
- `xchainpy_midgard`, `xchainpy_thornode`, `xchainpy_mayanode`, `xchainpy_midgard_maya` are generated API clients; regenerate via `make gen_midgard`, `make gen_thornode`, etc. (see `Makefile`, `scripts/common.sh`).
- Avoid manual edits inside generated model/api files unless absolutely necessary; prefer fixing generator inputs/scripts (`scripts/fix_swagger_spec.py`, `scripts/modify_setup.py`).

## Developer workflows (project-specific)
- Install dev tools: `make dev_tools` (runs `uv sync --group dev`).
- Install editable local packages for multi-package runs/tests: `make tc_env` (runs `uv sync --all-packages --group dev`).
- Run tests: `make test` (targets selected packages explicitly, not whole-repo discovery).
- Cross-Python matrix: `tox` (configured for `py39, py310, py311`, command delegates to `make test`).
- Build docs: `make doc`; docs import package modules via `docs/conf.py` `packages = [...]`, so missing local package dirs break docs build.
- Publish/version helpers are interactive (`make build`, `make publish`, `make upver`) and rely on scripts in `scripts/`.

## Conventions and patterns to preserve
- Async-first APIs: most network calls are `async`; tests rely on `pytest` + `pytest.mark.asyncio` with `asyncio_mode = auto` (`pytest.ini`).
- Keep chain/client neutrality by using `Chain`, `Asset`, `CryptoAmount`, `Amount` from `xchainpy2_utils` instead of ad-hoc primitives.
- Client constructors commonly accept `phrase` or `private_key` (mutually exclusive), `network`, and `wallet_index`; follow that signature style when adding chains.
- Network switching and explorer links are per-network dictionaries (`*_EXPLORERS`, URL maps in each client const module).
- Examples use environment variables (`PHRASE`, optional `THORNODE`) via `examples/common.py`.

## Integration points and external services
- THOR endpoints are centralized in `packages/xchainpy_thorchain_query/xchainpy2_thorchain_query/env.py`.
- Query clients patch headers (`X-Chain-Client`, user-agent) and add retries/timeouts via `patch_clients.py` and `ConfigurationEx`.
- EVM clients may use external providers (`web3` RPC + optional `ETHERSCAN_API_KEY` / `MORALIS_API_KEY` for richer history/token data).
- UTXO clients use provider round-robin/fallback patterns (`xchainpy2_client/utxo_client.py`, bitcoinlib service providers).

## Safe-edit guardrails for agents
- If adding a new chain package, also update wallet detection map in `packages/xchainpy_wallet/xchainpy2_wallet/detect_clients.py` and docs package lists (`docs/conf.py`, docs index files).
- Keep changes package-local unless the behavior crosses boundaries (e.g., base client contract changes require updates in inheriting chain packages + wallet/query call sites).
- Prefer validating with targeted package tests first, then `make test` for repo-wide confidence.
