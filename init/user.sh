#!/usr/bin/env bash

set -o xtrace
set -e

if [[ "$#" != "1" ]]; then
  echo "Usage: $0 <user>"
  exit 1
fi
MK_USER=$1

if ! getent passwd | grep -q $MK_USER; then
  # Create the user with a group and home directory
  useradd --user-group --create-home ${MK_USER}
fi
# Add to docker group to run docker commands
getent group docker || groupadd docker
usermod --append --groups docker misha
# Disable initial lecture to help with scripting
echo "Defaults: al !lecture" >> /etc/sudoers
# Add to sudo
echo "$MK_USER ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
