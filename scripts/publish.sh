#!/bin/bash
set -e

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
  clean_dist $1
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
  # Use the default value (all packages)
  PACKS=(../packages/xchainpy_*)
  echo "No package specified, available packages:"
  counter=1
  for i in "${PACKS[@]}"; do
    echo " $counter) $(basename $i) [$counter]"
    ((counter++))
  done
  echo "Which package do you want to publish (enter the number)?"
  # ask for the number
  read -r number
  # check if the number is valid
  if [ "$number" -gt "${#PACKS[@]}" ]; then
    echo "Invalid number"
    exit 1
  fi
  # get the package name
  PACKS=${PACKS[$number - 1]}
  echo "Selected package: $PACKS"
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
