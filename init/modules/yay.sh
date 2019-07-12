#!/usr/bin/env bash
command -v yay 1>/dev/null || return 0
alias y="yay"
alias y-remove-orphans="y -Rsn --noconfirm \$(y -Qdtq)"
