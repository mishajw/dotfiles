#!/usr/bin/env bash
if ! command -v rustup 1>/dev/null; then
  # TODO: move to install/no-aur
  curl https://sh.rustup.rs -sSf | sh
fi
