#!/usr/bin/env bash

set -e
if [[ "$#" != 1 ]]; then
  echo "Usage: $0 <output directory>"
fi

SIZE=$(xdpyinfo | grep dimensions | grep -P '\d+x\d+' -o | head -1)
IMAGE_DIRECTORY=$1 && mkdir -p $IMAGE_DIRECTORY
IMAGE="$IMAGE_DIRECTORY/lock-screen-$SIZE.png"

# Write image to stdout so caller knows where it's written
echo $IMAGE

# Don't recreate image
if [ -e $IMAGE ]; then
  exit
fi

# Create all-white image
convert -size $SIZE xc:#619eff $IMAGE
# Apply gradient
convert $IMAGE \
  \( +clone -fx '0.5-(int(j)/h)/2' \) \
  -compose multiply \
  -composite $IMAGE
