#!/bin/bash

set -e

shopt -s nullglob

# This directory.
SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd )"

# Planemo to install for test.
PLANEMO_INSTALL_TARGET="${PLANEMO_INSTALL_TARGET:-planemo}"

# By default use pyton setup.py install to install the library.
SETUP_COMMAND="${SETUP_COMMAND:-install}"

TOOLS_DEVTEAM="${TOOLS_DEVTEAM:-}"

# Initialize a temp directory for testing.
TEMP_DIR=`mktemp -d`
echo "Setting up test directory $TEMP_DIR"
cd "$TEMP_DIR"

PLANEMO_VIRTUAL_ENV="${PLANEMO_VIRTUAL_ENV:-$TEMP_DIR/planemo-venv}"
virtualenv "$PLANEMO_VIRTUAL_ENV"
. "$PLANEMO_VIRTUAL_ENV/bin/activate"
pip install "$PLANEMO_INSTALL_TARGET"

cd $SCRIPT_DIR/..
python setup.py "$SETUP_COMMAND"

if [ -z "$1" ];
then
    if [ -z "$TOOLS_DEVTEAM" ];
    then
        TOOLS_DEVTEAM="$TEMP_DIR/tools-devteam"
        git clone https://github.com/galaxyproject/tools-devteam.git "$TOOLS_DEVTEAM"
    fi
    TARGET_TOOL_DIRS=(tools/fastq_trimmer_by_quality tool_collections/galaxy_sequence_utils/fastq_combiner tool_collections/galaxy_sequence_utils/fastq_manipulation tool_collections/galaxy_sequence_utils/fastq_groomer tool_collections/galaxy_sequence_utils/fastq_filter)
else
    TARGET_TOOL_DIRS=("$1")
fi

for tool_dir in ${TARGET_TOOL_DIRS[@]}
do
    planemo test --no_conda_auto_init --no_cleanup --no_dependency_resolution "$TOOLS_DEVTEAM/$tool_dir"
done
