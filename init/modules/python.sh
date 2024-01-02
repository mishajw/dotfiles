#!/usr/bin/env bash
export DF_PYTHON_DIR="$df/.env"
export DF_PYTHON="$df/.env/bin/python"
export DF_PIP="$df/.env/bin/pip"
alias pip="pip3"

# pyenv setup
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
