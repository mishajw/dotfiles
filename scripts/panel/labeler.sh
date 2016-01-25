#!/bin/bash

label=$1

while [ 1 ]; do
  read input
  echo "$label$input"
done

