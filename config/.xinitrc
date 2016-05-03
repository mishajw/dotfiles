export LANG=en_GB.UTF-8

# Set the keymap
setxkbmap gb

# Stop pointer from being X sometimes
xsetroot -cursor_name left_ptr

$scr/start/x.sh

sxhkd &
exec bspwm
