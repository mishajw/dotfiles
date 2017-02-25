#!/bin/bash

TAG=$1

BUILD_DIR="$workd/Nascar_build/PanAndScanReplay/RelWithDebInfo"

RELEASE_NAME=PanAndScanReplay_$(date '+%Y_%m_%d')_$TAG

EXPORT_DIR="$workd/Releases/PanAndScanReplay/$RELEASE_NAME"

mkdir $EXPORT_DIR
cp $BUILD_DIR/PanAndScanReplay.exe $EXPORT_DIR/${RELEASE_NAME}.exe
cp $BUILD_DIR/PanAndScanReplay.pdb $EXPORT_DIR/${RELEASE_NAME}.pdb

if pwd | grep $nascar; then
  git tag -a $RELEASE_NAME -m "Release for $RELEASE_NAME"
fi

