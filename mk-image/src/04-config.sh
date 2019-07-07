#!/usr/bin/env bash

set -o xtrace
set -e

TIME_ZONE="Europe/London"
HOST_NAME="mla"
LOCALE="en_GB.UTF-8 UTF-8"
KEY_MAP="uk"

ln --symbolic --force /usr/share/zoneinfo/$TIME_ZONE /etc/localtime
echo $HOST_NAME > /etc/hostname
echo $LOCALE > /etc/locale.gen
echo KEYMAP=$KEY_MAP > /etc/vconsole.conf
mkinitcpio --preset linux
