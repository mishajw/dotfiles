#!/usr/bin/env bash
command -v cargo 1>/dev/null || return 0
alias c="cargo"
alias cr="c run"
alias cb="c build"
alias ct="c test"
alias cf="c fmt"
alias cck="c check"
cdoc() {
  original_path=$PWD

  cargo doc &&
    cd target/doc &&
    python -m http.server 8000 &
  local_pid=$!

  cd ~/.rustup/toolchains/stable-*/share/doc/rust/html &&
    python -m http.server 8001 &
  stdlib_pid=$!

  cd $original_path
  trap 'kill $local_pid $stdlib_pid; exit' SIGINT
  wait $local_pid $stdlib_pid
}
