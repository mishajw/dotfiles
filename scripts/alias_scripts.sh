#!/usr/bin/env bash

original_dir=$(pwd)
cd $(dirname $0)

for file in ./*.{sh,py}; do
  file_name=$(echo $file | sed 's/[a-z]\+$//g;s/[\./]//g')
  extension=$(echo $file | grep -Po '[^\.]+$')

  echo Making alias for $file called $file_name

  if [ "$extension" = "sh" ]; then
    alias $file_name="$(realpath $file)"
  elif [ "$extension" = "py" ]; then
    alias $file_name="$DF_PYTHON $(realpath $file)"
  else
    echo "Unrecognized file"
    exit -1
  fi
done

cd $original_dir
