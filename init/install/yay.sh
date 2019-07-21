#!/usr/bin/env bash

command -v yay 1>/dev/null && exit 0

cd "$(mktemp --directory)"
git clone https://aur.archlinux.org/yay.git . \
  && makepkg --syncdeps --install --needed --noconfirm
