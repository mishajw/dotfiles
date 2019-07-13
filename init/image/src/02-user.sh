#!/usr/bin/env bash

set -o xtrace
set -e

MK_USER=misha
if getent passwd | grep -q $MK_USER; then
  exit 0
fi

# Create the user with a group and home directory
useradd --user-group --create-home ${MK_USER}

echo "${MK_USER} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
