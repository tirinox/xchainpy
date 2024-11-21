#!/bin/bash

SWAGGER_LOCAL="./swagger-codegen-cli.jar"
SWAGGER_VERSION=3.0.52
SWAGGER_CODEGEN="https://repo1.maven.org/maven2/io/swagger/codegen/v3/swagger-codegen-cli/${SWAGGER_VERSION}/swagger-codegen-cli-${SWAGGER_VERSION}.jar"

function check_output_dir() {
  read -p "Do you want to clear ${OUTPUT_DIR}? (y/n) " yn
  case $yn in
  [yY])
    rm -rf "${OUTPUT_DIR}"
    return
    ;;
  [nN])
    if [ -n "$(ls -A ${OUTPUT_DIR})" ]; then
      echo "Output directory ${OUTPUT_DIR} is not empty. Aborting."
      exit 1
    fi
    ;;
  *) echo invalid response ;;
  esac

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
  read -p "Do you want install the package? (y/n) " yn
  case $yn in
  [yY])
    # python3 -m pip install --editable "${OUTPUT_DIR}"
    cd ${OUTPUT_DIR} || exit 3
    python3 setup.py develop

    return
    ;;
  [nN])
    return
    ;;
  *) echo invalid response ;;
  esac

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
  read -p "Do you want fix swagger spec to generate complete Python models? (y/n) " yn
  case $yn in
  [yY])
    # if package is xchainpy2_thornode then set mode = thor
    if [ "$PACKAGE_NAME" == "xchainpy2_thornode" ]; then
      SWAGGER_FIX_MODE="thor"
    # maya
    elif [ "$PACKAGE_NAME" == "xchainpy2_mayanode" ]; then
      SWAGGER_FIX_MODE="maya"
    # midgard
    elif [ "$PACKAGE_NAME" == "xchainpy2_midgard" ]; then
      SWAGGER_FIX_MODE="midgard"
    else
      # raise error
      echo "Invalid package name ($PACKAGE_NAME). Cannot set SWAGGER_FIX_MODE! Aborting."
      exit 1
    fi

    python3 fix_swagger_spec.py -i ${SWAGGER_FILE} -o ${SWAGGER_FIXED_FILE} -m ${SWAGGER_FIX_MODE}
    export SWAGGER_FILE=${SWAGGER_FIXED_FILE}
    return
    ;;
  [nN])
    return
    ;;
  *) echo invalid response ;;
  esac
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

  # Ask to install the package for development
  install_develop
}

function ask_dev_virtual_env() {
  read -p "Do you want to create new virtual environment and install dev tools? (y/n) " yn
  case $yn in
  [yY])
    python3 -m venv "../temp/venv"
    source "../temp/venv/bin/activate"
    pip install "betterproto[compiler]" betterproto
    pip install grpcio grpcio-tools
    ;;
  *) ;;
  esac
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
  # Use the default value (all packages)
  PACKS=(../packages/xchainpy_*)
  N=3 # Set the number of columns
  COLUMN_WIDTH=40 # Adjust column width as needed

  echo "Available packages:"

  counter=1
  column=1

  for i in "${PACKS[@]}"; do
    # Print the current package in the column format
    printf "%-$((COLUMN_WIDTH - 1))s" "$counter) $(basename "$i")"

    # Check if we reached the last column or the last package
    if (( column == N )); then
      echo # Move to the next row
      column=1
    else
      ((column++))
    fi
    ((counter++))
  done

  # Print a newline if the last row is incomplete
  if (( column > 1 && column <= N )); then
    echo
  fi

  echo "Which package do you want to select (enter the number)?"

  # Ask for the number
  read -r number

  # Check if the number is not valid
  if ! [[ "$number" =~ ^[0-9]+$ ]]; then
    echo "Invalid input: not a number."
    return
  elif (( number < 1 || number > ${#PACKS[@]} )); then
    echo "Invalid input: number out of range."
    return
  fi

  # Get the package name
  SELECTED_PACKAGE=${PACKS[$number - 1]}
  echo "Selected package: $SELECTED_PACKAGE"
}
