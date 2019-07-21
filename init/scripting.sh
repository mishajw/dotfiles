#!/usr/bin/env bash

# Quick directories
export df="$HOME/dotfiles"
export cnf="$df/config"
export scr="$df/scripts"
export imgs="$df/images"
export init="$df/init"
export local="$df/local"
export prog="$HOME/prog" && mkdir -p $prog
export dflogs="/tmp/dflogs" && mkdir -p $dflogs
export perm="$HOME/.perm"
export lperm="$HOME/.local-perm"

# Display and sound names
export DISPLAY1_NAME="eDP1"
export DISPLAY2_NAME="DP2"
export DISPLAY2_X="1920"
export DISPLAY2_Y="1080"
export DISPLAY2_HZ="60"
export DISPLAY2_REL="--above $DISPLAY1_NAME"
export MASTER_SOUND="Master"

# Window manager
export BACKGROUND_IMAGE="$imgs/backgrounds/boat-builders.jpg"
export LOCK_MODE="gradient"
export SXHKD_SHELL="bash"
export WINDOW_GAP=15
export WINDOW_RESIZE_INCREMENTS=200
export VOLUME_FIFO="/tmp/df_volume_fifo"

# Misc
export IP_DEVICE="wlan0"
export EDITOR="vim"
export LANG=en_GB.UTF-8
export LANGUAGE="$LANG"
export LC_ALL="$LANG"
export MAIN_FONT="Monospace:style=Bold:size=10"
export SCREENSHOT_LOCATION="/tmp/scr.png"
export CHROME_SCALE_FACTOR="1.2"
export SYSTEM_PYTHON=$(which python3)
export SCREENSHOT_COMMAND='import $SCREENSHOT_LOCATION'

# Default applications for use in dotfiles
export TERMINAL="termite"
export BROWSER="google-chrome-stable --force-device-scale-factor=\$CHROME_SCALE_FACTOR"

export PATH="$PATH:$HOME/.cargo/bin"

[ -f $local/scripting.sh ] && source $local/scripting.sh

pacman_install() {
  sudo pacman -S $@ --noconfirm --needed
}

source $init/modules/python.sh
source $init/modules/go.sh
