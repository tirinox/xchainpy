#!/bin/bash

# 1. Make sure, that grpcio and grpcio-tools are installed
# python3 -m pip install grpcio grpcio-tools
# 2. Download somewhere THORNode source code
# And set TC_PATH env variable to the path of the downloaded source code of THORNode

set -e

source common.sh

LAST_THOR_VERSION="release-1.134.0"
LAST_MAYA_VERSION="v1.110.0"
COSMOS_SDK_VERSION="v0.45.1"

THOR_GIT="https://gitlab.com/thorchain/thornode.git"
MAYA_GIT="https://gitlab.com/mayachain/mayanode.git"
COSMOS_GIT="https://github.com/cosmos/cosmos-sdk.git"

TEMP="../temp"

echo "I will help you to generate Python code from THORNode/Maya protobuf files"

# ask if user wants to create new venv
ask_dev_virtual_env

# -----------------------
# ask for protocol

echo "Please, select the protocol you want to generate code for:"
echo "1. THORChain"
echo "2. Maya"

read -p "Your choice? " protocode

case $protocode in
1)
  PROTOCOL=thorchain
  LAST_VERSION=$LAST_THOR_VERSION
  GIT_URL=$THOR_GIT
  ;;
2)
  PROTOCOL=mayachain
  LAST_VERSION=$LAST_MAYA_VERSION
  GIT_URL=$MAYA_GIT
  ;;
*)
  echo "Invalid choice"
  exit 1
  ;;
esac

# -----------------------

NODE_CODE="$TEMP/node_code_$PROTOCOL"
COSMOS_CODE="$TEMP/cosmos"

if [ ! -d "$NODE_CODE" ]; then
  git clone $GIT_URL $NODE_CODE
  cd $NODE_CODE && git checkout $LAST_VERSION && cd ..
  echo "Source code downloaded"
fi

if [ ! -d "$COSMOS_CODE" ]; then
  git clone $COSMOS_GIT $COSMOS_CODE
  cd $COSMOS_CODE && git checkout $COSMOS_SDK_VERSION && cd ..
  echo "Cosmos source code downloaded"
fi

# -----------------------
# are you sure?
echo "I will generate code for $PROTOCOL"
PROTO_OUT_PATH="../packages/xchainpy_$PROTOCOL/xchainpy2_$PROTOCOL/proto"
echo "Input path: $NODE_CODE"
echo "Output path: $PROTO_OUT_PATH"
read -p "Are you sure? (y/n) " yn

case $yn in
[yY])
  # print working directory
  pwd

  mkdir -p $PROTO_OUT_PATH

  ls $TEMP

  $TEMP/venv/bin/python3 -m grpc_tools.protoc --proto_path="${NODE_CODE}/proto" \
    --proto_path="${NODE_CODE}/third_party/proto" \
    --proto_path="${COSMOS_CODE}/proto" \
    --python_out="${PROTO_OUT_PATH}" --grpc_python_out="${PROTO_OUT_PATH}" --pyi_out="${PROTO_OUT_PATH}" \
    "$PROTOCOL/v1/x/$PROTOCOL/types/msg_deposit.proto" \
    "$PROTOCOL/v1/x/$PROTOCOL/types/msg_send.proto" \
    "$PROTOCOL/v1/common/common.proto" "gogoproto/gogo.proto" "cosmos/base/v1beta1/coin.proto"


  touch_inits $PROTO_OUT_PATH
  # restore root __init__.py as it contains code to have the proto files module available
  git restore "$PROTO_OUT_PATH/__init__.py"
  ;;
*)
  exit 1
  ;;
esac

# -----------------------
echo "Done!"
