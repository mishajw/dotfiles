#!/usr/bin/env bash
[ ! -d /Users ] && return
source $init/modules/brew.sh
bindkey "∆" history-beginning-search-forward
bindkey "˚" history-beginning-search-backward
