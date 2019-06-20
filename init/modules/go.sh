#!/usr/bin/env bash
command -v go 1>/dev/null || return
export GOROOT=$(go env | grep GOROOT | sed 's/GOROOT=//g;s/"//g')
export GOPATH=$HOME/src/go
export PATH=$GOPATH/bin:$GOROOT/bin:$PATH
mkdir -p $GOPATH
