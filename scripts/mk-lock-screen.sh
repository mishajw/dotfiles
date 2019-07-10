#!/usr/bin/env bash

if [[ "$#" != 1 ]]; then
  echo "Usage: $0 <output file>"
fi

img=$1
size=$(xdpyinfo | grep dimensions | grep -P '\d+x\d+' -o | head -1)

# Create all-white image
convert -size $size xc:white $img
# Apply gradient
convert $img \( +clone -fx '0.5-(int(j)/h)/2' \) -compose multiply -composite $img
