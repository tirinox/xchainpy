#!/bin/bash

SWAGGER_LOCAL="./swagger-codegen-cli.jar"
SWAGGER_VERSION=3.0.47
SWAGGER_CODEGEN="https://repo1.maven.org/maven2/io/swagger/codegen/v3/swagger-codegen-cli/${SWAGGER_VERSION}/swagger-codegen-cli-${SWAGGER_VERSION}.jar"

function check_output_dir() {
  read -p "Do you want to clear ${OUTPUT_DIR}? (y/n) " yn
  case $yn in
  [yY])
    rm -rf ${OUTPUT_DIR}
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
    --additional-properties packageName=${PACKAGE_NAME},aiohttp=true,snake-case-methods=true,python36=true,packageVersion=${VERSION}
}

function install_develop() {
  read -p "Do you want install the package? (y/n) " yn
  case $yn in
  [yY])
    python3 -m pip install --editable "${OUTPUT_DIR}"
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
  cp "../LICENSE" "${OUTPUT_DIR}/LICENSE"
}

function fix_swagger_spec() {
  read -p "Do you want fix swagger spec to generate complete Python models? (y/n) " yn
  case $yn in
  [yY])
    python3 fix_swagger_spec.py -i ${SWAGGER_FILE} -o ${SWAGGER_FIXED_FILE}
    export SWAGGER_FILE=${SWAGGER_FIXED_FILE}
    return
    ;;
  [nN])
    return
    ;;
  *) echo invalid response ;;
  esac
}

function run_codegen() {
  # Download swagger codegen jar if it is missing
  download_swagger_codegen

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
