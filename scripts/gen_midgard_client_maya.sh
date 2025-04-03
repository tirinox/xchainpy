#!/bin/sh

OUTPUT_DIR="../packages/xchainpy_midgard_maya/"
PACKAGE_NAME="xchainpy2_midgard_maya"
SWAGGER_FILE="https://midgard.mayachain.info/v2/swagger.json"
SWAGGER_FIXED_FILE="./apispecs/midgard_maya.yaml"

source "common.sh"
run_codegen
