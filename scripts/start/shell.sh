#!/bin/bash

source $HOME/dotfiles/exports.sh
source $HOME/dotfiles/aliases.sh

# Start x if it isn't already started
pgrep Xorg 1>/dev/null || ( [ -z "$TMUX" ] && startx)

