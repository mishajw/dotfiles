#!/usr/bin/env bash

display-start() {
  mode_name="custom_${DISPLAY2_X}x${DISPLAY2_Y}_${DISPLAY2_HZ}"
  echo "Adding mode $mode_name"
  eval xrandr --newmode $mode_name \
    $(gtf $DISPLAY2_X $DISPLAY2_Y $DISPLAY2_HZ |
      grep Modeline |
      sed -E 's/Modeline "[^ ]*" +//g')
  xrandr --addmode $DISPLAY2_NAME $mode_name
  xrandr --output $DISPLAY2_NAME --mode $mode_name
  eval xrandr --output $DISPLAY2_NAME $DISPLAY2_REL
  opr $cnf/bspwmrc
}

display-stop() {
  xrandr --output $DISPLAY2_NAME --off
  opr $cnf/bspwmrc
}
