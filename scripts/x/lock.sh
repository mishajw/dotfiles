#!/usr/bin/env bash

set -e
IMAGE="$gen/lock-screen.png"

if [ "$LOCK_MODE" == "blur" ]; then
  scrot $IMAGE
  convert $IMAGE -scale 25% -blur 0x10 -scale 400% $IMAGE
elif [ "$LOCK_MODE" == "pixel" ]; then
  scrot $IMAGE
  convert $IMAGE -scale 5% -scale 2000% $IMAGE
elif [ "$LOCK_MODE" == "gradient" ]; then
  IMAGE=$($scr/util/mk-lock-screen.sh $gen)
fi

i3lock --ignore-empty-password --image $IMAGE

if [ "$LOCK_MODE" != "gradient" ]; then
  rm $IMAGE
fi
