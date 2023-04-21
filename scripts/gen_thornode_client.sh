#!/bin/sh

OUTPUT_DIR="../packages/xchainpy_thornode/"
PACKAGE_NAME="thornode_client"
SWAGGER_FILE="https://thornode.ninerealms.com/thorchain/doc/openapi.yaml"

source "common.sh"
run_codegen