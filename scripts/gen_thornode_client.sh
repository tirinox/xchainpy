#!/bin/sh

OUTPUT_DIR="../packages/xchainpy_thornode/"
PACKAGE_NAME="thornode_client"
SWAGGER_FILE="https://thornode.ninerealms.com/thorchain/doc/openapi.yaml"

source "common.sh"

download_swagger_codegen

# Check if output directory is empty
check_output_dir

# Do job
codegen_client $OUTPUT_DIR $PACKAGE_NAME $SWAGGER_FILE

install_develop
