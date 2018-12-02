#!/usr/bin/env bash

for file in $scr/*.{sh,py}; do
  file_name="$(echo ${file%.*} | sed 's/.*\///')"
  extension="${file##*.}"
  echo "Making alias for $file called $file_name"
  if [ "$extension" = "sh" ]; then
    alias $file_name="$file"
  elif [ "$extension" = "py" ]; then
    alias $file_name="$DF_PYTHON $file"
  else
    echo "Unrecognized file"
    exit -1
  fi
done
