#!/bin/sh

# 1. Make sure, that grpcio and grpcio-tools are installed
# python3 -m pip install grpcio grpcio-tools
# 2. Download somewhere THORNode source code
# And set TC_PATH env variable to the path of the downloaded source code of THORNode
DEFAULT_TC_PATH="$HOME/Downloads/thornode-release-1.114.0"
TC_PATH="${1:-$DEFAULT_TC_PATH}"

OUT_PATH="../packages/xchainpy_thorchain/xchainpy2_thorchain/proto"

#PROTO_FILES=$(find "$TC_PATH" -type f -name "*.proto" | awk '{printf "%s ", $0}')

python3 -m grpc_tools.protoc --proto_path="${TC_PATH}/proto" \
  --proto_path="${TC_PATH}/third_party/proto" \
  --python_out="${OUT_PATH}" --grpc_python_out="${OUT_PATH}" --pyi_out="${OUT_PATH}" \
  "thorchain/v1/x/thorchain/types/msg_deposit.proto" \
  "thorchain/v1/common/common.proto" "gogoproto/gogo.proto"

find "$OUT_PATH/" -type d -exec touch {}/__init__.py \;
# restore root __init__.py as it contains code to have the proto files module available
git restore "$OUT_PATH/__init__.py"