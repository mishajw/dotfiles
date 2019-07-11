#!/usr/bin/env bash
[ "$(uname)" != "Darwin" ] && return 0
source $init/modules/brew.sh
bindkey "∆" history-beginning-search-forward
bindkey "˚" history-beginning-search-backward
bindkey "¬" forward-word
bindkey "˙" backward-word
