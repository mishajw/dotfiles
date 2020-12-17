#!/usr/bin/env bash

# Check the system python version
python_version=$($SYSTEM_PYTHON -V)
if [[ \
    $python_version != *"3.6"* && \
    $python_version != *"3.7"* && \
    $python_version != *"3.8"* && \
    $python_version != *"3.9"* ]]; then
  echo "Bad python version: $python_version"
  exit 1
fi

# If the python directory already exists, we're done
if [ -d $DF_PYTHON_DIR ]; then
  exit 0
fi

# Set up the virtual env
$SYSTEM_PYTHON -m venv $DF_PYTHON_DIR
$DF_PIP install --requirement $init/packages/python
$DF_PIP install --upgrade pip
