#!/usr/bin/env bash

set -o xtrace
set -e

TIME_ZONE="Europe/London"
HOST_NAME="mla"
LOCALE="en_GB.UTF-8 UTF-8"
KEY_MAP="uk"

modify_mkinitcpio_conf() {
  HOOKS=$(cat /etc/mkinitcpio.conf | grep -P '^HOOKS=' | sed 's/HOOKS=(//g;s/)//g')

  # Require keyboard and udev
  echo $HOOKS | grep -q keyboard || exit 1
  echo $HOOKS | grep -q udev || exit 1

  echo $HOOKS

  # Place keymap after keyboard
  if ! echo $HOOKS | grep -q keymap; then
    HOOKS=$(echo $HOOKS | sed 's/keyboard/keyboard keymap/g')
  fi

  # Place ecnrypt and lvm2 at end
  if ! echo $HOOKS | grep -q encrypt; then
    HOOKS="${HOOKS} encrypt"
  fi
  if ! echo $HOOKS | grep -q lvm2; then
    HOOKS="${HOOKS} lvm2"
  fi

  sed "s/^HOOKS=.*/HOOKS=($HOOKS)/g" --in-place /etc/mkinitcpio.conf
}

ln --symbolic --force /usr/share/zoneinfo/$TIME_ZONE /etc/localtime
echo $HOST_NAME > /etc/hostname
echo $LOCALE > /etc/locale.gen
echo KEYMAP=$KEY_MAP > /etc/vconsole.conf
locale-gen

modify_mkinitcpio_conf
mkinitcpio --preset linux
