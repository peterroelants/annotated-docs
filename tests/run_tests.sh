#!/usr/bin/env bash
# Run with `./test/run_tests.sh`

set -e  # Exit if anything fails

TEST_DIR=$(dirname "$(readlink -f "$0")")  # Test directory path
cd ${TEST_DIR}

# Run tests
echo "Run Pytest for '${TEST_DIR}'"
pytest -o log_cli=false -vv ${TEST_DIR}
