#!/usr/bin/env bash
command -v exa 1>/dev/null || return
alias ls="exa --color=always --git"
alias ll="ls -l"
alias la="ls -la"
alias lt="ls -T"
