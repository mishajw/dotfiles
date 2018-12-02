#!/usr/bin/env bash

source /home/misha/dotfiles/init/scripting.sh

if [[ "$(bspc config -d focused window_gap)" == "0" ]]; then
  bspc config -d focused window_gap $WINDOW_GAP
  echo "Adding gap"
else
  bspc config -d focused window_gap 0
  echo "Removing gap"
fi

