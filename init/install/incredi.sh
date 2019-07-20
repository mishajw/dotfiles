#!/usr/bin/env bash
set -e
command -v incredi 1>/dev/null && exit 1
pacman --needed --noconfirm -S csfml
cargo install --git https://github.com/mishajw/incredi-panel.git
