#!/bin/sh

OUTPUT_DIR="../packages/xchainpy_midgard/"
PACKAGE_NAME="midgard_client"
SWAGGER_FILE="https://midgard.mayachain.info/v2/swagger.json"

source "common.sh"

download_swagger_codegen

# Check if output directory is empty
check_output_dir

# Do job
codegen_client $OUTPUT_DIR $PACKAGE_NAME $SWAGGER_FILE

install_develop
