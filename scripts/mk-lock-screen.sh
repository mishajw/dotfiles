#!/usr/bin/env bash

set -e
if [[ "$#" != 1 ]]; then
  echo "Usage: $0 <output file>"
fi

IMAGE=$1
SIZE=$(xdpyinfo | grep dimensions | grep -P '\d+x\d+' -o | head -1)

# Create all-white image
convert -size $SIZE xc:#619eff $IMAGE
# Apply gradient
convert $IMAGE \
  \( +clone -fx '0.5-(int(j)/h)/2' \) \
  -compose multiply \
  -composite $IMAGE
