#!/usr/bin/env bash
command -v brew 1>/dev/null || return 0

brew-permissions() {
  sudo chown -R $(whoami) \
    /usr/local/bin \
    /usr/local/etc \
    /usr/local/sbin \
    /usr/local/share \
    /usr/local/share/doc
}

alias b="brew"
alias bi="brew-permissions && brew install"
