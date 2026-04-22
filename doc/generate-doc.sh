#!/bin/bash

set -eu


## works both under bash and sh
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")


SRC_DIR="$SCRIPT_DIR/../src"


generate_help() {
    echo "generating help output"

    HELP_PATH="${SCRIPT_DIR}"/cmdargs.md
    
    cd "$SRC_DIR"
    
    COMMAND="python3 -m mdlinkscheck"
    COMMAND_TEXT="checkmdlinks"
    
    echo "## $COMMAND_TEXT --help" > "${HELP_PATH}"
    echo -e "\`\`\`" >> "${HELP_PATH}"
    $COMMAND --help >> "${HELP_PATH}"
    echo -e "\`\`\`" >> "${HELP_PATH}"
    
    sed -i "s/__main__.py/${COMMAND_TEXT}/g" "${HELP_PATH}"
}


generate_help


"${SCRIPT_DIR}"/generate_small.sh
