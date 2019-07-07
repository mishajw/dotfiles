#!/usr/bin/env bash

set -o xtrace
set -e

# Install pacstrap, genfstab, arch-chroot
pacman -S arch-install-scripts --noconfirm --needed
# TODO: rank mirrors
pacstrap /mnt base base-devel
genfstab -U /mnt >> /mnt/etc/fstab
