#!/bin/sh

OUTPUT_DIR="../packages/xchainpy_mayanode/"
PACKAGE_NAME="mayanode_client"
SWAGGER_FILE="https://mayanode.mayachain.info/mayachain/doc/openapi.yaml"

source "common.sh"

download_swagger_codegen

# Check if output directory is empty
check_output_dir

# Do job
codegen_client $OUTPUT_DIR $PACKAGE_NAME $SWAGGER_FILE

install_develop
