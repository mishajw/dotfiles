#!/usr/bin/env bash
command -v exa 1>/dev/null || return 0
alias ls="exa --color=always"
alias ll="ls -l"
alias la="ls -la"
alias lt="ls -T"
