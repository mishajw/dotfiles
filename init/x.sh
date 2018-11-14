#!/usr/bin/env bash
$scr/util/fix_intellij.sh
xset b off
setxkbmap gb
# Stop pointer from being X sometimes
xsetroot -cursor_name left_ptr
