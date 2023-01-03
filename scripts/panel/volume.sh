#!/usr/bin/env bash

# Function to print the volume
print-vol() {
  echo -n "vol: "
  amixer sget Master | grep "Mono: Playback" | grep -Po "[0-9]+%"
}

# Set up FIFO
rm $VOLUME_FIFO
mkfifo $VOLUME_FIFO

# Start print loop
print-vol
cat $VOLUME_FIFO | while read line; do print-vol; done
