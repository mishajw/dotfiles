#!/usr/bin/env bash
command -v yaourt 1>/dev/null || return 0
alias y="yaourt"
alias y-remove-orphans="y -Rsn --noconfirm \$(y -Qdtq)"
