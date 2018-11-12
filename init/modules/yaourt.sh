#!/usr/bin/env bash
command -v yaourt 1>/dev/null || return
alias y="yaourt"
alias y-remove-orphans="y -Rsn --noconfirm \$(y -Qdtq)"
