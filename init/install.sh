#!/usr/bin/env bash

set -e

$init/install/yay.sh
yay --noconfirm --needed -S $(cat $init/packages/arch | grep -Pv '^#')

$init/install/python.sh
$init/install/vim.sh
$init/install/rustup.sh
$init/install/incredi.sh

echo "Finished installing, not including AUR packages"
