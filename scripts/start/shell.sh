#!/bin/bash

source /home/misha/dotfiles/exports.sh
source /home/misha/dotfiles/aliases.sh

# Start x if it isn't already started
pgrep Xorg 1>/dev/null || ( [ -z "$TMUX" ] && startx)

