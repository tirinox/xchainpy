#!/bin/sh

OUTPUT_DIR="../packages/xchainpy_mayanode/"
PACKAGE_NAME="xchainpy2_mayanode"
SWAGGER_FILE="https://mayanode.mayachain.info/mayachain/doc/openapi.yaml"
SWAGGER_FIXED_FILE="./apispecs/mayanode.yaml"
VERSION=1.107.1

source "common.sh"
run_codegen