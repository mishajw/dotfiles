#!/usr/bin/env bash

set -o xtrace
set -e

if [[ "$#" != 1 ]]; then
  echo "Usage: $0 <qcow2 path>"
  exit 1
fi
IMAGE=$1

pacman -S qemu-headless --noconfirm --needed
if mount | grep -q /mnt; then
  exit 0
fi
modprobe nbd
qemu-nbd --connect /dev/nbd0 $IMAGE
mount /dev/nbd0 /mnt
if file $IMAGE | grep -q ext4; then
  exit 0
fi
mkfs.ext4 $IMAGE
