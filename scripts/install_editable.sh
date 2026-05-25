#!/bin/bash
set -e
source common.sh
ask_for_package
UV=${UV:-uv}
cd ..
${UV} venv --allow-existing
${UV} pip install --editable "scripts/${SELECTED_PACKAGE}"
