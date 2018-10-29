#!/usr/bin/env bash

original_dir=$(pwd)
cd $(dirname $0)

if [ ! -d ".env" ]; then
  python3 -m venv .env
  ./.env/bin/pip install -r requirements.txt
fi

for file in ./*.{sh,py}; do
  file_name=$(echo $file | sed 's/[a-z]\+$//g;s/[\./]//g')
  extension=$(echo $file | grep -Po '[^\.]+$')

  echo Making alias for $file called $file_name

  if [ "$extension" = "sh" ]; then
    alias $file_name="$(realpath $file)"
  elif [ "$extension" = "py" ]; then
    alias $file_name="$(realpath .env/bin/python) $(realpath $file)"
  else
    echo "Unrecognized file"
    exit -1
  fi
done

cd $original_dir

