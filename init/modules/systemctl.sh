#!/usr/bin/env bash
command -v systemctl 1>/dev/null || return 0
alias sc="sudo systemctl"
