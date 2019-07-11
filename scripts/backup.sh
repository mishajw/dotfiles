#!/usr/bin/env bash

if [ $# -lt 1 ]; then
  echo "Usage: $0 <file to backup> <optional -r>"
  return 0
fi

FILE_TO_BACKUP=$1
REMOVE_ORIGINAL=false

if [ "$2" = "-r" ]; then
  REMOVE_ORIGINAL=true
fi

DATE=$(date +"%Y%m%d_%H%M%S")

if $REMOVE_ORIGINAL; then
  mv $FILE_TO_BACKUP ${FILE_TO_BACKUP}_$DATE
else
  cp -r $FILE_TO_BACKUP ${FILE_TO_BACKUP}_$DATE
fi
