#!/usr/bin/env bash

py-calc() {
  if [[ "$#" == "0" ]]; then
    echo "Usage: $0 <maths>"
    return 1
  fi
  MATHS="$@"
  $DF_PYTHON -c "from math import *; print($MATHS)"
}

alias calc="noglob py-calc"
