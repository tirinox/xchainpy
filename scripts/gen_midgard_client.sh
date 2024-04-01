#!/bin/sh

OUTPUT_DIR="../packages/xchainpy_midgard/"
PACKAGE_NAME="xchainpy2_midgard"
SWAGGER_FILE="https://midgard.ninerealms.com/v2/swagger.json"
SWAGGER_FILE_MAYA="https://midgard.mayachain.info/v2/swagger.json"
SWAGGER_FIXED_FILE="./apispecs/midgard.yaml"
VERSION=2.20.1

source "common.sh"
run_codegen
