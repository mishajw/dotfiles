#!/usr/bin/env bash
command -v systemctl 1>/dev/null || return
alias sysstart="sudo systemctl start"
alias sysstop="sudo systemctl stop"
alias sysres="sudo systemctl restart"
