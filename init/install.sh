#!/usr/bin/env bash
set -e
$init/install/vim.sh
brew bundle --file $df/config/Brewfile
chsh -s $(which zsh)
