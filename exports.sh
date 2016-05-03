#!/bin/bash

# Display
export MAIN_DISPLAY="eDP1"
export SECOND_DISPLAY="DP2"
export SECOND_DISPLAY_RES="1920x1080"

# Sound
export MASTER_SOUND="Master"

# Quick directories
export df="/home/misha/dotfiles"
export cnf="$df/config"
export scr="$df/scripts"

# Directories
export PANEL_PATH="$df/panel"
export PANEL_FIFO="/tmp/panel-fifo"

# Visuals
export MAIN_FONT="Monospace:style=Bold:size=10"
export BAR_HEIGHT=25
export BACKGROUND_IMAGE="$df/background.jpg"

# Misc
export LANGUAGE="$LANG"
export LC_ALL="$LANG"
export PATH=$PATH:/usr/bin/core_perl:$SCRIPTS
export SXHKD_SHELL="bash"

# SVN
export SVN_EDITOR="gvim"

source $df/local-exports.sh

