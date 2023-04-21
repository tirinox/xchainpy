#!/bin/sh

OUTPUT_DIR="../packages/xchainpy_mayanode/"
PACKAGE_NAME="mayanode_client"
SWAGGER_FILE="https://mayanode.mayachain.info/mayachain/doc/openapi.yaml"

source "common.sh"
run_codegen