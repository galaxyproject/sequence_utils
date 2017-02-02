#!/bin/bash

set -e

shopt -s nullglob

# This directory.
SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd )"

# Planemo to install for test.
PLANEMO_INSTALL_TARGET="${PLANEMO_INSTALL_TARGET:-planemo==0.37.0}"

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
deactivate

ENV_DIR="$TEMP_DIR/dependencies/galaxy_sequence_utils/dev"
mkdir -p "$ENV_DIR"
cat "$SCRIPT_DIR/planemo_test_env.sh" | sed -e "s#_temp_dir_#/$TEMP_DIR#" > "$ENV_DIR/env.sh"
ln -s dev "$TEMP_DIR/dependencies/galaxy_sequence_utils/default"

virtualenv "$ENV_DIR/venv"
. "$ENV_DIR/venv/bin/activate"

cd $SCRIPT_DIR/..
python setup.py "$SETUP_COMMAND"

## TODO: Add option to test a wheel instead.
# pip install $SCRIPT_DIR/../dist/*whl

cat "$SCRIPT_DIR/planemo_test_dependency_resolvers_conf_template.xml" | sed -e "s#_temp_dir_#$TEMP_DIR#" > "$TEMP_DIR/dependency_resolvers_conf.xml"


. "$PLANEMO_VIRTUAL_ENV/bin/activate"

if [ -z "$TOOLS_DEVTEAM" ];
then
    TOOLS_DEVTEAM="$TEMP_DIR/tools-devteam"
    git clone https://github.com/galaxyproject/tools-devteam.git "$TOOLS_DEVTEAM"
fi

for tool_dir in tools/fastq_trimmer_by_quality tool_collections/galaxy_sequence_utils/fastq_combiner
do
    planemo test --dependency_resolvers_config_file "$TEMP_DIR/dependency_resolvers_conf.xml" "$TOOLS_DEVTEAM/$tool_dir"
done
