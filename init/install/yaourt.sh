#!/usr/bin/env bash

command -v yaourt 1>/dev/null && return 0

PACKAGE_QUERY=$(mktemp --directory)
YAOURT=$(mktemp --directory)

git clone https://aur.archlinux.org/package-query.git $PACKAGE_QUERY \
  && cd $PACKAGE_QUERY \
  && makepkg --syncdeps --install --needed --noconfirm

git clone https://aur.archlinux.org/yaourt.git $YAOURT \
  && cd $YAOURT \
  && makepkg --syncdeps --install --needed --noconfirm
