#!/bin/sh

set -e

BIN_PATH=`dirname "$0"`
BIN_PATH=`cd "${BIN_PATH}"; pwd`

if [ "$1" = "" ]; then
    echo "Error: need data_dir_path"
    exit 1
fi

operation_type="flat_insert"
PYTHON=python3
$PYTHON $BIN_PATH/../lib/ssb_test/starrocks_table_operation.py $operation_type $1
