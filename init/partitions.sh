#!/usr/bin/env bash

set -o xtrace
set -e

BOOT_SIZE_MB=200
SWAP_SIZE_MB=$((256))

if [[ "$#" != 3 ]]; then
  echo "Usage: $0 <device> <partition mode> <main partition size in MiB>"
  exit 1
fi
DEVICE=$1
PARTITION_MODE=$2
MAIN_SIZE_MB=$3

if ! command -v parted 1>/dev/null; then
  echo "parted must be installed"
  exit 1
fi

simple() {
  BOOT_START_MB=1
  SWAP_START_MB=$(($BOOT_START_MB + $BOOT_SIZE_MB))
  MAIN_START_MB=$(($SWAP_START_MB + $SWAP_SIZE_MB))
  ALL_END_MB=$(($MAIN_START_MB + $MAIN_SIZE_MB))
  parted $DEVICE mklabel gpt
  parted $DEVICE mkpart primary ext4 \
    ${BOOT_START_MB}MiB ${SWAP_START_MB}MiB
  parted $DEVICE mkpart primary linux-swap \
    ${SWAP_START_MB}MiB ${MAIN_START_MB}MiB
  parted $DEVICE mkpart primary ext4 \
    ${MAIN_START_MB}MiB ${ALL_END_MB}MiB
  parted $DEVICE set 1 esp on
  parted $DEVICE print
}

split() {
  SWAP_START_MB=$((1 + $BOOT_SIZE_MB))
  MAIN_START_MB=$(($SWAP_START_MB + $SWAP_SIZE_MB))
  ALL_END_MB=$(($MAIN_START_MB + $MAIN_SIZE_MB))
  parted $DEVICE mklabel gpt
  parted $DEVICE mkpart primary ext4 \
    ${BOOT_START_MB}MiB ${SWAP_START_MB}MiB
  parted $DEVICE mkpart primary linux-swap \
    ${SWAP_START_MB}MiB ${MAIN_START_MB}MiB
  parted $DEVICE mkpart primary ext4 \
    ${MAIN_START_MB}MiB ${ALL_END_MB}MiB
  parted $DEVICE set 1 esp on
  parted $DEVICE print
}

if [[ "$PARTITION_MODE" == "simple" ]]; then
  simple
elif [[ "$PARTITION_MODE" == "split" ]]; then
  
else
  echo "Unrecognized partition mode $PARTITION_MODE"
  exit 1
fi
