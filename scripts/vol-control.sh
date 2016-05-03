#!/bin/bash

MODE=$1
CHANGE_AMOUNT=5

if [ "$MODE" == "up" ]; then
  MODIFIER="$CHANGE_AMOUNT%+"
elif [ "$MODE" == "down" ]; then
  MODIFIER="$CHANGE_AMOUNT%-"
elif [ "$MODE" == "toggle" ]; then
  MODIFIER="toggle"
else 
  echo "No valid command specified: up, down, toggle"
  exit
fi

amixer sset Master $MODIFIER > /dev/null
echo "VolumeWidget" > $PANEL_FIFO

