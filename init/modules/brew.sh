#!/usr/bin/env bash
[ -e /opt/homebrew/bin/brew ] 1>/dev/null || return 0
eval "$(/opt/homebrew/bin/brew shellenv)"
alias b="brew"
alias bi="brew install"
alias bf="brew bundle --file ~/dotfiles/config/Brewfile dump -f"
