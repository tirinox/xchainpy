#!/bin/bash
set -e

source common.sh

echo "---------------"
echo "This script will update the version of the Python package"

ask_for_package
PACKAGE_DIR=$SELECTED_PACKAGE

echo "---------------"

# make sure that "pyproject.toml" exists
if [ ! -f $PACKAGE_DIR/pyproject.toml ]; then
    echo "pyproject.toml not found in $PACKAGE_DIR"
    exit 1
fi

# open pyproject.toml and read the version
VERSION=$(cat $PACKAGE_DIR/pyproject.toml | grep "version" | cut -d '"' -f 2)

echo "Current version: $VERSION"

# increment the version
NEW_VERSION=$(python -c "version = '$VERSION'.split('.'); version[-1] = str(int(version[-1]) + 1); print('.'.join(version))")

echo "New version: $NEW_VERSION"

# ask if sure
read -p "Are you sure you want to update the version? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    exit 1
fi

# update the version, $VERSION can contain periods, so escape them
python -c "import re; import sys; file_path = '$PACKAGE_DIR/pyproject.toml'; content = open(file_path).read(); new_content = re.sub(r'version = \"$VERSION\"', f'version = \"$NEW_VERSION\"', content); open(file_path, 'w').write(new_content)"



