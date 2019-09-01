#!/usr/bin/env bash
run-intellij() {
  (
    cd $HOME &&
    $scr/util/fix-intellij.sh &&
    opr $INTELLIJ)
}
