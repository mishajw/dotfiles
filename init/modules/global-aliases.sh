#!/usr/bin/env bash
alias -g G='| grep'
alias -g Gi='| grep -i'
alias -g L="| less"
alias -g C="| wc -l"
alias -g Se="2>&1"
alias -g Ps="\$(ps -axo 'pid args' | awk 'NR!=1' | fzf | awk '{print \$1}')"
