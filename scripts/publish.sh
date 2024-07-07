#!/bin/bash
set -e

source common.sh

function build() {
  echo "---------------"
  echo "Building $1"
  python3 -m build "$1"
}

function publish_test() {
  build $1
  echo "---------------"
  echo "Publishing $1"
  python -m twine upload --repository testpypi "$1"/dist/*
}

function clean_dist() {
  rm $1/dist/*.tar.gz
  rm $1/dist/*.whl
}

function publish() {
  clean_dist $1 || true
  build $1

  echo "---------------"
  echo "Publishing $1"
  python -m twine upload --repository pypi "$1"/dist/*
}

# Check if the script has at least two arguments
if [ "$#" -ge 2 ]; then
  # Use the second positional argument as the value for PACKS
  PACKS="../packages/$2"
else
  ask_for_package
fi

# Case commands
case "$1" in

build)
  build "$PACKS"
  ;;
publish)
  publish "$PACKS"
  ;;

publish_test)
  publish_test "$PACKS"
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
