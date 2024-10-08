#!/bin/bash

## TODO: fail if virtualenv is not located.

set -e

VERSION=$1

# Ensure working directory is galaxy-lib project.
SCRIPTS_DIRECTORY="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIRECTORY="${SCRIPTS_DIRECTORY}/.."
DIST_DIRECTORY="${PROJECT_DIRECTORY}/dist"
WHEEL_FILE="${DIST_DIRECTORY}/galaxy_sequence_utils-$VERSION-py2.py3-none-any.whl"
DEV_REQUIREMENTS="${PROJECT_DIRECTORY}/dev-requirements.txt"

cd $PROJECT_DIRECTORY


WORKING_DIRECTORY=`mktemp -d -t testXXXXXX`
cp -r "$PROJECT_DIRECTORY"/{.coveragerc,setup.cfg,tests} "$WORKING_DIRECTORY"

cd "$WORKING_DIRECTORY"
VIRTUALENV_DIRECTORY="$WORKING_DIRECTORY/venv"
python3 -m venv "$VIRTUALENV_DIRECTORY"
. "$VIRTUALENV_DIRECTORY/bin/activate"
pip install "${WHEEL_FILE}"
pip install -r "${DEV_REQUIREMENTS}"

pytest
