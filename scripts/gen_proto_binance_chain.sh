#!/bin/bash

set -e
source common.sh

TEMP="../temp"
INPUT_DIR="../packages/xchainpy_binance/proto"
PROTO_OUT_PATH="../packages/xchainpy_binance/xchainpy2_binance/sdk/proto"

echo "I will help you to generate Python code from Binance chain protobuf files"

# ask if user wants to create new venv
ask_dev_virtual_env

# -----------------------

# are you sure?
echo "I will generate code for Binance"
echo "Input path: $INPUT_DIR"
echo "Output path: $PROTO_OUT_PATH"
read -p "Are you sure? (y/n) " yn

case $yn in
[yY])
  # print working directory
  pwd

  mkdir -p $PROTO_OUT_PATH
  $TEMP/venv/bin/python3 -m grpc_tools.protoc \
    --proto_path="$INPUT_DIR" \
    --python_out="${PROTO_OUT_PATH}" --grpc_python_out="${PROTO_OUT_PATH}" --pyi_out="${PROTO_OUT_PATH}" \
    "dex.proto"

  touch_inits $PROTO_OUT_PATH

  ;;
*)
  exit 1
  ;;
esac

# -----------------------
echo "Done!"
