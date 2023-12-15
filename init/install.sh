#!/usr/bin/env bash
set -e
$init/install/vim.sh
brew bundle --file $df/config/Brewfile
python3 scripts/make-symlinks.py --symlinks config/symlinks.json
chsh -s $(which zsh)

yabai --start-service
skhd --start-service
