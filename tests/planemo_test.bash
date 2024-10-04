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

# Create a temporary virtual env for Galaxy and sequence_utils
GALAXY_VIRTUAL_ENV="$TEMP_DIR/galaxy-venv"
python3 -m venv "$GALAXY_VIRTUAL_ENV"
export GALAXY_VIRTUAL_ENV

# Install Planemo
PLANEMO_VIRTUAL_ENV="${PLANEMO_VIRTUAL_ENV:-$TEMP_DIR/planemo-venv}"
python3 -m venv "$PLANEMO_VIRTUAL_ENV"
. "$PLANEMO_VIRTUAL_ENV/bin/activate"
python3 -m pip install "$PLANEMO_INSTALL_TARGET"

# Set up Galaxy for Planemo
GALAXY_ROOT="${GALAXY_ROOT:-$TEMP_DIR/galaxy}"
GALAXY_BRANCH="${GALAXY_BRANCH:-dev}"
planemo ci_setup --galaxy_root "$GALAXY_ROOT" --galaxy_branch "$GALAXY_BRANCH"

# Install sequence_utils into Galaxy virtual env
cd $SCRIPT_DIR/..
. "$GALAXY_VIRTUAL_ENV/bin/activate"
python3 -m pip install --upgrade .

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

. "$PLANEMO_VIRTUAL_ENV/bin/activate"
planemo test --galaxy_root "$GALAXY_ROOT" --galaxy_branch "$GALAXY_BRANCH" --no_conda_auto_init --no_cleanup --no_dependency_resolution "${TARGET_TOOL_DIRS[@]}"
