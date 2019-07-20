#!/usr/bin/env bash

$init/install/yay.sh
yay -S --needed --noconfirm $init/packages/arch

$init/install/zsh.sh
$init/install/python.sh
$init/install/vim.sh
$init/install/rustup.sh
$init/install/incredi.sh
