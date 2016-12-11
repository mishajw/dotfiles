#!/bin/bash

scrot /tmp/screen.png
convert /tmp/screen.png -scale 25% -blur 0x10 -scale 400% /tmp/screen.png
convert /tmp/screen.png $imgs/lock.png -gravity center -composite -matte /tmp/screen.png

i3lock -t -e -f -u -i /tmp/screen.png

rm /tmp/screen.png

