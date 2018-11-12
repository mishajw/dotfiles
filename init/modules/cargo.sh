#!/usr/bin/env bash
command -v cargo 1>/dev/null || return
alias c="cargo"
alias cr="c run"
alias cb="c build"
alias ct="c test"
alias cf="c +nightly fmt"
alias cck="c check"
