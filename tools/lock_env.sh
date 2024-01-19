#!/usr/bin/env bash

ROOT_PATH=$(dirname $(dirname "$(readlink -f "$0")"))  # Root directory path
cd ${ROOT_PATH}

set -eu

echo -e "\nExporting environment to ${ROOT_PATH}/env/env.lock.yml"

conda env export --no-builds | grep -v "^prefix: " > ${ROOT_PATH}/env/env.lock.yml
