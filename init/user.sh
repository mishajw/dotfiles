#!/usr/bin/env bash

set -o xtrace
set -e

if [[ "$#" != "1" ]]; then
  echo "Usage: $0 <user>"
  exit 1
fi
MK_USER=$1

if getent passwd | grep -q $MK_USER; then
  exit 0
fi
# Create the user with a group and home directory
useradd --user-group --create-home ${MK_USER}
