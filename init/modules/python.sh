#!/usr/bin/env bash

export DF_PYTHON_DIR="$df/.env"
export DF_PYTHON="$df/.env/bin/python"
export DF_PIP="$df/.env/bin/pip"

# Check the system python version
python_version=$($SYSTEM_PYTHON -V)
if [[ $python_version != *"3.6"* ]]; then
  echo "Bad python version: $python_version"
  return
fi

# If the python directory already exists, we're done
if [ -d $DF_PYTHON_DIR ]; then
  return
fi

# Set up the virtual env
$SYSTEM_PYTHON -m venv $DF_PYTHON_DIR
$DF_PIP install --requirement python-requirements.txt
