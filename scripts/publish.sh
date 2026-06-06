#!/bin/bash
set -e

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"

source "${SCRIPT_DIR}/common.sh"

UV=${UV:-uv}

function load_publish_env() {
  local env_file

  for env_file in \
    "${REPO_ROOT}/.env.publish.local" \
    "${REPO_ROOT}/.env.publish" \
    "${REPO_ROOT}/.env"; do
    if [ -f "${env_file}" ]; then
      set -a
      # shellcheck disable=SC1090
      source "${env_file}"
      set +a
    fi
  done
}

function require_publish_token() {
  if [ -z "${UV_PUBLISH_PASSWORD}" ]; then
    echo "Missing UV_PUBLISH_PASSWORD. Add it to .env.publish.local/.env.publish/.env or export it before running publish."
    exit 1
  fi

  export UV_PUBLISH_USERNAME=${UV_PUBLISH_USERNAME:-__token__}
}

function build() {
  echo "---------------"
  echo "Building $1"
  ${UV} build "$1" --out-dir "$1/dist"
}

function publish_test() {
  require_publish_token
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
  require_publish_token
  clean_dist $1 || true
  build $1

  echo "---------------"
  echo "Publishing $1"
  ${UV} publish "$1"/dist/*
}

load_publish_env

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
