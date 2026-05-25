#!/bin/bash
set -e

source common.sh

UV=${UV:-uv}

function build() {
  echo "---------------"
  echo "Building $1"
  ${UV} build "$1" --out-dir "$1/dist"
}

function publish_test() {
  build $1
  echo "---------------"
  echo "Publishing $1"
  ${UV} publish --publish-url https://test.pypi.org/legacy/ "$1"/dist/*
}

function clean_dist() {
  rm -f $1/dist/*.tar.gz
  rm -f $1/dist/*.whl
}

function publish() {
  clean_dist $1 || true
  build $1

  echo "---------------"
  echo "Publishing $1"
  ${UV} publish "$1"/dist/*
}

# Check if the script has at least two arguments
if [ "$#" -ge 2 ]; then
  # Use the second positional argument as the value for PACKS
  SELECTED_PACKAGE="../packages/$2"
else
  ask_for_package
fi

# Case commands
case "$1" in

build)
  build "$SELECTED_PACKAGE"
  ;;
publish)
  publish "$SELECTED_PACKAGE"
  ;;

publish_test)
  publish_test "$SELECTED_PACKAGE"
  ;;

*)
  echo "Usage: $0 command PACKAGE"
  echo "Commands:"
  echo "  help             Show this help message"
  echo "  build            Build packages"
  echo "  publish          Publish packages"
  echo "  publish_test     Publish packages to the test repository"
  exit 0
  ;;
esac
