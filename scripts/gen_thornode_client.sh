#!/bin/sh

OUTPUT_DIR="../packages/xchainpy_thornode/"
PACKAGE_NAME="xchainpy2_thornode"
SWAGGER_FILE="https://thornode.ninerealms.com/thorchain/doc/openapi.yaml"
SWAGGER_FIXED_FILE="./apispecs/thornode.yaml"
VERSION=1.125.0

source "common.sh"
run_codegen
