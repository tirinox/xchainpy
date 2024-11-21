#!/bin/bash
set -e
source common.sh
ask_for_package
python3 -m pip install --editable $SELECTED_PACKAGE
