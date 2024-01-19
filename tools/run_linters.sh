#!/usr/bin/env bash
# Run with `./tools/run_checks.sh`

ROOT_PATH=$(dirname $(dirname "$(readlink -f "$0")"))  # Root directory path
cd ${ROOT_PATH}

set -eu

echo -e "\nRun ruff code formatting checks"

ruff check ${ROOT_PATH}/src ${ROOT_PATH}/tests

echo -e "\nRun mypy type checks"
mypy ${ROOT_PATH}/src ${ROOT_PATH}/tests
