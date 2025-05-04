#!/bin/bash

SWAGGER_LOCAL="./swagger-codegen-cli.jar"
SWAGGER_VERSION=3.0.52
SWAGGER_CODEGEN="https://repo1.maven.org/maven2/io/swagger/codegen/v3/swagger-codegen-cli/${SWAGGER_VERSION}/swagger-codegen-cli-${SWAGGER_VERSION}.jar"

ask_yes_no() {
  local prompt="$1"
  local default="$2"  # "yes" or "no"
  local answer

  while true; do
    if [[ "$default" == "yes" ]]; then
      read -p "$prompt [Y/n] " answer
    elif [[ "$default" == "no" ]]; then
      read -p "$prompt [y/N] " answer
    else
      read -p "$prompt [y/n] " answer
    fi

    # If no answer is given, use the default.
    answer=${answer:-$default}

    # Convert answer to lowercase using tr.
    local answer_lower
    answer_lower=$(echo "$answer" | tr '[:upper:]' '[:lower:]')

    case "$answer_lower" in
      y|yes)
        return 0  # Yes: return success.
        ;;
      n|no)
        return 1  # No: return failure.
        ;;
      *)
        echo "Please answer yes or no."
        ;;
    esac
  done
}

function check_output_dir() {
  if ask_yes_no "Do you want to clear ${OUTPUT_DIR}?" "yes"; then
    rm -rf "${OUTPUT_DIR}"
  else
    if [ -n "$(ls -A ${OUTPUT_DIR})" ]; then
      echo "Output directory ${OUTPUT_DIR} is not empty. Aborting."
      exit 1
    fi
  fi
}

function codegen_client() {
  #  swagger-codegen generate \
  java -jar swagger-codegen-cli.jar generate \
    -i ${SWAGGER_FILE} \
    -l python \
    -o ${OUTPUT_DIR} \
    --library asyncio \
    --additional-properties packageName=${PACKAGE_NAME},aiohttp=true,snake-case-methods=true,python36=true,packageVersion=${VERSION},readmeFile=README.md
}

function install_develop() {
  if ask_yes_no "Do you want to install the package for development?" "no"; then
    # python3 -m pip install --editable "${OUTPUT_DIR}"
    cd ${OUTPUT_DIR} || exit 3
    python3 setup.py develop
  fi
}

function download_swagger_codegen() {
  if [ ! -f "${SWAGGER_LOCAL}" ]; then
    wget ${SWAGGER_CODEGEN} -O swagger-codegen-cli.jar
  fi
}

function add_license() {
  # echo pwd
  echo `pwd`
  echo "Copying LICENSE to ${OUTPUT_DIR}"
  cp "../LICENSE" "${OUTPUT_DIR}"
}

function fix_swagger_spec() {
  if ask_yes_no "Do you want to fix swagger spec to generate complete Python models?" "yes"; then
    # if package is xchainpy2_thornode then set mode = thor
    if [ "$PACKAGE_NAME" == "xchainpy2_thornode" ]; then
      SWAGGER_FIX_MODE="thor"
    # maya
    elif [ "$PACKAGE_NAME" == "xchainpy2_mayanode" ]; then
      SWAGGER_FIX_MODE="maya"
    # midgard
    elif [ "$PACKAGE_NAME" == "xchainpy2_midgard" ]; then
      SWAGGER_FIX_MODE="midgard"
    elif [ "$PACKAGE_NAME" == "xchainpy2_midgard_maya" ]; then
      SWAGGER_FIX_MODE="midgard"
    else
      # raise error
      echo "Invalid package name ($PACKAGE_NAME). Cannot set SWAGGER_FIX_MODE! Aborting."
      exit 1
    fi

    python3 fix_swagger_spec.py -i ${SWAGGER_FILE} -o ${SWAGGER_FIXED_FILE} -m ${SWAGGER_FIX_MODE}
    export SWAGGER_FILE=${SWAGGER_FIXED_FILE}
  fi
}

function check_java_runtime() {
  # Check if Java is installed and enabled
  if ! java -version &> /dev/null; then
    echo "Java is not installed or enabled. Aborting script."
    echo "For macOS, you can install Java using 'brew install java'"
    exit 1
  fi
}

function run_codegen() {
  # Check Java
  check_java_runtime

  # Download swagger codegen jar if it is missing
  download_swagger_codegen

  # Set package VERSION var
  set_version

  # Ask to fix swagger spec
  fix_swagger_spec

  # Check if output directory is empty
  check_output_dir

  # Do job
  codegen_client "$OUTPUT_DIR" "$PACKAGE_NAME" "$SWAGGER_FILE"
  add_license

  # Fix setup.py file
  fix_setup_py

  # Ask to install the package for development
  install_develop
}

function ask_dev_virtual_env() {
  # check if exists
  if [ ! -d "../temp/venv" ]; then
    echo "Virtual environment does not exist."
    DEFAULT="yes"
  else
    DEFAULT="no"
  fi

  if ask_yes_no "Do you want to create new virtual environment and install dev tools?" $DEFAULT; then
    python3 -m venv "../temp/venv"
    source "../temp/venv/bin/activate"
    pip install "betterproto[compiler]" betterproto
    pip install grpcio grpcio-tools
  fi
}

function touch_inits() {
  find "$1/" -type d -exec touch {}/__init__.py \;
}

function set_version() {
  VERSION=$(python get_ver_from_spec.py $SWAGGER_FILE)
  echo "Version: ${VERSION}"
}

function invalid_number() {
    echo "Invalid number. Must be greater in range 1-${#PACKS[@]}"
    exit 1
}

function ask_for_package() {
    SELECTED_PACKAGE=$(python3 ask_package.py 2>/dev/tty)
    # check empty
    if [ -z "$SELECTED_PACKAGE" ]; then
        echo "No package selected. Aborting."
        exit 1
    fi
}


function fix_setup_py() {
  if ask_yes_no "Do you want to fix setup.py?" "yes"; then
    python3 modify_setup.py "${OUTPUT_DIR}/setup.py"
  fi
}
