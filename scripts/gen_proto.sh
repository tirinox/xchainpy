#!/bin/bash

# 1. Make sure, that grpcio and grpcio-tools are installed
# python3 -m pip install grpcio grpcio-tools

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

source common.sh

LAST_THOR_VERSION="v3.18.1"
LAST_MAYA_VERSION="v1.129.3"
COSMOS_SDK_VERSION="v0.53.0"
COSMOS_PROTO_VERSION="v1.0.0-beta.5"

THOR_GIT="https://gitlab.com/thorchain/thornode.git"
MAYA_GIT="https://gitlab.com/mayachain/mayanode.git"
COSMOS_GIT="https://github.com/cosmos/cosmos-sdk.git"
COSMOS_PROTO_GIT="https://github.com/cosmos/cosmos-proto.git"
GOGOPROTO_GIT="https://github.com/cosmos/gogoproto.git"

TEMP="../temp"

checkout_ref() {
  local repo_path="$1"
  local ref="$2"

  git -C "$repo_path" fetch --tags --force --quiet origin
  git -C "$repo_path" checkout --force --quiet "$ref"
}

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
COSMOS_PROTO_CODE="$TEMP/cosmos-proto"
GOGOPROTO_CODE="$TEMP/gogoproto"

mkdir -p "$TEMP"

if [ ! -d "$NODE_CODE" ]; then
  git clone "$GIT_URL" "$NODE_CODE"
  echo "Source code downloaded"
fi
checkout_ref "$NODE_CODE" "$LAST_VERSION"

if [ ! -d "$COSMOS_CODE" ]; then
  git clone "$COSMOS_GIT" "$COSMOS_CODE"
  echo "Cosmos source code downloaded"
fi
checkout_ref "$COSMOS_CODE" "$COSMOS_SDK_VERSION"

if [ ! -d "$COSMOS_PROTO_CODE" ]; then
  git clone "$COSMOS_PROTO_GIT" "$COSMOS_PROTO_CODE"
  echo "Cosmos Proto source code downloaded"
fi
checkout_ref "$COSMOS_PROTO_CODE" "$COSMOS_PROTO_VERSION"

if [ ! -d "$GOGOPROTO_CODE" ]; then
  git clone "$GOGOPROTO_GIT" "$GOGOPROTO_CODE"
  echo "Gogoproto source code downloaded"
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

  mkdir -p "$PROTO_OUT_PATH"

  ls "$TEMP"

  "$TEMP/venv/bin/python3" -m grpc_tools.protoc --proto_path="${NODE_CODE}/proto" \
    --proto_path="${NODE_CODE}/proto/${PROTOCOL}/v1" \
    --proto_path="${GOGOPROTO_CODE}" \
    --proto_path="${COSMOS_PROTO_CODE}/proto" \
    --proto_path="${COSMOS_CODE}/proto" \
    --python_out="${PROTO_OUT_PATH}" --grpc_python_out="${PROTO_OUT_PATH}" --pyi_out="${PROTO_OUT_PATH}" \
    "common/common.proto" "gogoproto/gogo.proto" "amino/amino.proto" "cosmos_proto/cosmos.proto" "cosmos/base/v1beta1/coin.proto" \
    "$PROTOCOL/v1/types/msg_deposit.proto" \
    "$PROTOCOL/v1/types/msg_send.proto"


  touch_inits "$PROTO_OUT_PATH"
  # restore root __init__.py as it contains code to have the proto files module available
  git restore "$PROTO_OUT_PATH/__init__.py"
  ;;
*)
  echo "Aborting"
  exit 1
  ;;
esac

# -----------------------
echo "Done!"
