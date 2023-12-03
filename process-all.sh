#!/bin/bash

set -eu


## works both under bash and sh
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")


$SCRIPT_DIR/src/testmdlinkscheck/runtests.py

$SCRIPT_DIR/tools/checkall.sh

$SCRIPT_DIR/generate-all.sh


echo "processing completed"
