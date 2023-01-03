#!/usr/bin/env bash

if [ $# != 1 ]; then
  echo "Usage: $0 <increment, [-1, 1]>"
  exit -1
fi
INCREMENT=$1
NEW_LEVEL=$(xrandr --verbose | grep 'Brightness' -m 1 | awk "{
  level = \$2 + $INCREMENT;
  if (level > 1) {
    level = 1;
  }
  if (level < 0) {
    level = 0;
  }
  print level
}")

xrandr \
  | awk '$2 == "connected" {print $1}' \
  | xargs -I% xrandr --output % --brightness $NEW_LEVEL
