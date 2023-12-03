#!/bin/bash

set -eu


## works both under bash and sh
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")


cd $SCRIPT_DIR


./codecheck.sh
./doccheck.sh
./typecheck.sh

echo -e "\nchecking links in MD files"
python3 -m mdlinkscheck -d .. --excludes ".*/tmp/.*" ".*/src/test.*/.*" ".*/venv/.*"


echo -e "\neverything is fine"
