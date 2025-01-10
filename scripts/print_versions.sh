#!/bin/bash

# Function to extract project.version from pyproject.toml
extract_version() {
    local file="$1"
    # Use grep and sed to extract the version line and clean it
    grep -E '^\s*version\s*=' "$file" | sed -E "s/^\s*version\s*=\s*['\"](.*)['\"]$/\1/"
}

# Prepare header for the table
printf "%-54s | %-20s\n" "File" "Version"
echo "$(printf '=%.0s' {1..50}) | $(printf '=%.0s' {1..20})"

# Walk through all subdirectories and find pyproject.toml files
find "../packages" -type f -name "pyproject.toml" | while read -r filepath; do
    # Extract and print version with the file path
    version=$(extract_version "$filepath")
    if [[ -n "$version" ]]; then
        printf "%-54s | %-20s\n" "$filepath" "$version"
    else
        printf "%-54s | %-20s\n" "$filepath" "Not Found"
    fi
done
