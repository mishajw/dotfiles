#!/usr/bin/env bash

#
# Creates and mounts a qcow2 image. Primarily used for debugging image creation.
#

set -e

if [[ "$#" != 2 ]]; then
  echo "Usage: $0 <size, e.g. 10G> <output>"
  exit 1
fi
SIZE=$1
OUTPUT=$2

echo "Making qcow2"
qemu-img create -f qcow2 $OUTPUT $SIZE

echo "Setting up nbd device"
modprobe nbd
qemu-nbd --connect /dev/nbd1 $OUTPUT

echo "Created qcow2 at $OUTPUT, mounted at /dev/nbd1"
