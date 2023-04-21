#!/bin/sh

OUTPUT_DIR="../packages/xchainpy_midgard/"
PACKAGE_NAME="midgard_client"
SWAGGER_FILE="https://midgard.mayachain.info/v2/swagger.json"

source "common.sh"
run_codegen
