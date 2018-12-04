#!/usr/bin/env bash
[ "$(uname)" != "Darwin" ] && return
source $init/modules/brew.sh
bindkey "∆" history-beginning-search-forward
bindkey "˚" history-beginning-search-backward
