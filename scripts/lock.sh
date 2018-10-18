#!/usr/bin/env bash

IMAGE="/tmp/screen.png"

scrot $IMAGE
if [ "$LOCK_MODE" == "blur" ]; then
  convert $IMAGE -scale 25% -blur 0x10 -scale 400% $IMAGE
elif [ "$LOCK_MODE" == "pixel" ]; then
  convert $IMAGE -scale 5% -scale 2000% $IMAGE
fi

i3lock --ignore-empty-password --image $IMAGE
rm $IMAGE

