#!/usr/bin/env bash

bspc node --focus last &&
  xdotool key Up &&
  sleep 0.1 &&
  xdotool key Return &&
  bspc node --focus last.local

