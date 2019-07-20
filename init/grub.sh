#!/usr/bin/env bash

set -e
set -o xtrace

if [[ "$#" != 1 ]]; then
  echo "Usage: $0 <device>"
  exit 1
fi
DEVICE=$1

pacman --needed --noconfirm grub
grub-install --recheck --target=i386-pc $DEVICE
grub-mkconfig -o /boot/grub/grub.cfg
