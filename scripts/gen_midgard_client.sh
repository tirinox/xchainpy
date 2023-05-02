#!/bin/sh

OUTPUT_DIR="../packages/xchainpy_midgard/"
PACKAGE_NAME="xchainpy2_midgard"
SWAGGER_FILE="https://midgard.mayachain.info/v2/swagger.json"
SWAGGER_FIXED_FILE="./apispecs/midgard.yaml"

source "common.sh"
run_codegen
