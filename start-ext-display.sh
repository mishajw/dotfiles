#!/bin/bash

xrandr --addmode $SECOND_DISPLAY $SECOND_DISPLAY_RES
xrandr --output $SECOND_DISPLAY --mode $SECOND_DISPLAY_RES --above $MAIN_DISPLAY
$cnf/bspwmrc

