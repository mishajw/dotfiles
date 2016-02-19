#!/bin/bash

source $PANEL_PATH/widgets/panelParams.py

while true ; do
  date +'%a %d %b %I:%M:%S %p'
  sleep $SLEEP_CLOCK
done
