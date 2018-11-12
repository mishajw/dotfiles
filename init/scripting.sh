#!/usr/bin/env bash

# Quick directories
export df="$HOME/dotfiles"
export cnf="$df/config"
export scr="$df/scripts"
export imgs="$df/images"
export init="$df/init"
export prog="$HOME/prog" && mkdir -p $prog

# Display and sound names
export MAIN_DISPLAY="eDP1"
export SECOND_DISPLAY="DP2"
export SECOND_DISPLAY_X="1920"
export SECOND_DISPLAY_Y="1080"
export SECOND_DISPLAY_HZ="60"
export MASTER_SOUND="Master"

# Window manager
export BACKGROUND_IMAGE="$imgs/backgrounds/boat-builders.jpg"
export LOCK_MODE="pixel"
export PANEL_FIFO="/tmp/panel-fifo"
export PANEL_HEIGHT=25
export SXHKD_SHELL="bash"
export WINDOW_GAP=15

# Misc
export EDITOR="vim"
export LANGUAGE="$LANG"
export LC_ALL="$LANG"
export MAIN_FONT="Monospace:style=Bold:size=10"
export PATH=$PATH:/usr/bin/core_perl
export SCREENSHOT_LOCATION="/tmp/scr.png"

[ -f $init/local_scripting.sh ] && source $init/local_scripting.sh
