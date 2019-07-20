#!/usr/bin/env bash
set -e
if ! command -v exa 1>/dev/null; then
  curl https://sh.rustup.rs -sSf | sh
fi
rustup toolchain install stable
rustup default stable
