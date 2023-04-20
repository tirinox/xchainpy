#!/bin/bash

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
    --additional-properties packageName=${PACKAGE_NAME},aiohttp=true,snake-case-methods=true,python36=true
}

function install_develop() {
  read -p "Do you want install the package? (y/n) " yn
  case $yn in
  [yY])
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

SWAGGER_LOCAL="./swagger-codegen-cli.jar"
SWAGGER_VERSION=3.0.41
SWAGGER_CODEGEN="https://repo1.maven.org/maven2/io/swagger/codegen/v3/swagger-codegen-cli/${SWAGGER_VERSION}/swagger-codegen-cli-${SWAGGER_VERSION}.jar"

function download_swagger_codegen() {
  if [ ! -f "${SWAGGER_LOCAL}" ]; then
     wget ${SWAGGER_CODEGEN} -O swagger-codegen-cli.jar
  fi
}
