#!/usr/bin/env bash

display-start() {
  MODE_NAME="${SECOND_DISPLAY_X}x${SECOND_DISPLAY_Y}_${SECOND_DISPLAY_HZ}"
  echo "Adding mode $MODE_NAME"
  xrandr --newmode $MODE_NAME \
    `gtf $SECOND_DISPLAY_X $SECOND_DISPLAY_Y $SECOND_DISPLAY_HZ | \
      grep Modeline | \
      sed -E 's/Modeline "[^ ]*"//g'`
  xrandr --addmode $SECOND_DISPLAY $MODE_NAME
  xrandr --output $SECOND_DISPLAY --mode $MODE_NAME --above $MAIN_DISPLAY
  $cnf/bspwmrc
}

display-stop() {
  xrandr --output $SECOND_DISPLAY --off
  $cnf/bspwmrc
}
