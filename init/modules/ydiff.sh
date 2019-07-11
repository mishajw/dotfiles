#!/usr/bin/env bash
$DF_PIP freeze | grep -i ydiff > /dev/null || return 0
alias yd="python -m ydiff --side-by-side --width 100"
alias yds="git diff --staged | python -m ydiff --side-by-side --width 100"
