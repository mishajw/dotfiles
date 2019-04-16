#!/usr/bin/env bash

#
# This script assumes an internet connection and correctly partitioned disks
#

read -p "Device file to install on: " dev

mount /dev/$dev /mnt

# Install arch and base packages on device
pacstrap -i /mnt base base-devel

# Generate FSTAB file
genfstab -U /mnt >>/mnt/etc/fstab

echo "Done. Run 'arch-chroot /mnt' and run the root script."
