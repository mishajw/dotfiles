#!/usr/bin/env bash
command -v exa 1>/dev/null || return
alias ls="exa --git"
alias ll="ls -l"
alias la="ls -la"
