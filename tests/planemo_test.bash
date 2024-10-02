#!/bin/bash

set -e

shopt -s nullglob

# This directory.
SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd )"

# Planemo to install for test.
PLANEMO_INSTALL_TARGET="${PLANEMO_INSTALL_TARGET:-planemo}"

TOOLS_DEVTEAM="${TOOLS_DEVTEAM:-}"
TOOLS_IUC="${TOOLS_IUC:-}"

# Initialize a temp directory for testing.
TEMP_DIR=`mktemp -d`
echo "Setting up test directory $TEMP_DIR"
cd "$TEMP_DIR"

PLANEMO_VIRTUAL_ENV="${PLANEMO_VIRTUAL_ENV:-$TEMP_DIR/planemo-venv}"
virtualenv "$PLANEMO_VIRTUAL_ENV"
. "$PLANEMO_VIRTUAL_ENV/bin/activate"
pip install "$PLANEMO_INSTALL_TARGET"

cd $SCRIPT_DIR/..
pip install .

if [ -z "$1" ]; then
    if [ -z "$TOOLS_DEVTEAM" ]; then
        TOOLS_DEVTEAM="$TEMP_DIR/tools-devteam"
        git clone --depth=1 https://github.com/galaxyproject/tools-devteam.git "$TOOLS_DEVTEAM"
    fi
    if [ -z "$TOOLS_IUC" ]; then
        TOOLS_IUC="$TEMP_DIR/tools-iuc"
        git clone --depth=1 https://github.com/galaxyproject/tools-iuc.git "$TOOLS_IUC"
    fi
    TARGET_TOOL_DIRS=(
        "$TOOLS_DEVTEAM/tools/fastq_trimmer_by_quality"
        "$TOOLS_IUC/tool_collections/galaxy_sequence_utils/fastq_combiner"
        "$TOOLS_IUC/tool_collections/galaxy_sequence_utils/fastq_manipulation"
        "$TOOLS_IUC/tool_collections/galaxy_sequence_utils/fastq_groomer"
        "$TOOLS_IUC/tool_collections/galaxy_sequence_utils/fastq_filter"
    )
else
    TARGET_TOOL_DIRS=("$1")
fi

for tool_dir in ${TARGET_TOOL_DIRS[@]}; do
    planemo test --no_conda_auto_init --no_cleanup --no_dependency_resolution "$tool_dir"
done
