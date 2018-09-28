#!/bin/bash

source $HOME/dotfiles/exports.sh
source $HOME/dotfiles/aliases.sh

# Start x if it isn't already started
pgrep X 1>/dev/null || ([ -z "$TMUX" ] && startx)

