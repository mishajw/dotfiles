#!/bin/bash

# Display
export MAIN_DISPLAY="eDP1"
export SECOND_DISPLAY="DP2"
export SECOND_DISPLAY_X="1920"
export SECOND_DISPLAY_Y="1080"
export SECOND_DISPLAY_HZ="60"
export WINDOW_GAP=15

# Sound
export MASTER_SOUND="Master"

# Quick directories
export df="$HOME/dotfiles"
export cnf="$df/config"
export scr="$df/scripts"
export imgs="$df/images"

# Directories
export PANEL_PATH="$df/panel"
export PANEL_FIFO="/tmp/panel-fifo"

# Visuals
export MAIN_FONT="Monospace:style=Bold:size=10"
export PANEL_HEIGHT=25
export BACKGROUND_IMAGE="$imgs/backgrounds/boat-builders.jpg"
export SCREENSHOT_LOCATION="/tmp/scr.png"

# Misc
export EDITOR="vim"
export LANGUAGE="$LANG"
export LC_ALL="$LANG"
export PATH=$PATH:/usr/bin/core_perl:$SCRIPTS
export SXHKD_SHELL="bash"
export LOCK_MODE="pixel"

source $df/local-exports.sh

