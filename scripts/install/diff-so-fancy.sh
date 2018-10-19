#!/usr/bin/env bash

set -e
URL="https://raw.githubusercontent.com/so-fancy/diff-so-fancy/master/third_party/build_fatpack/diff-so-fancy"
INSTALL_DIR="$prog/diff-so-fancy"
INSTALL_PATH="$INSTALL_DIR/diff-so-fancy"
mkdir -p $INSTALL_DIR
curl $URL > $INSTALL_PATH
chmod +x $INSTALL_PATH

