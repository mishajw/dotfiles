#!/usr/bin/env bash

# TODO: We currently set up symlinks in three places:
# - here
# - init/config.sh
# - scripts/make-symlinks.py
# These shold be unified.

set -e

if [[ ! -e "$lperm" ]]; then
  echo "Making local perm at $lperm"
  mkdir -p \
    $lperm/src \
    $lperm/google-chrome \
    $lperm/media \
    $lperm/dotfiles \
    $lperm/downloads \
    $lperm/gnupg \
    $lperm/ssh \
    $lperm/idea-config
  touch $lperm/zsh_history
fi

if [[ ! -e "$perm" ]]; then
  echo "Making perm link at $perm"
  ln --symbolic --force $lperm $perm
fi

create_perm_link() {
  perm_dir=$1
  user_dir=$2
  if [[ ! -e $user_dir || -h $user_dir ]]; then
    echo "Making symlink from $user_dir to $perm_dir"
    ln --symbolic --force --no-dereference $perm_dir $user_dir
  fi
}
create_perm_link $perm/src $HOME/src
mkdir --parents $HOME/.config
create_perm_link $perm/google-chrome $HOME/.config/google-chrome
create_perm_link $perm/media $HOME/media
create_perm_link $perm/dotfiles $HOME/dotfiles
create_perm_link $perm/downloads $HOME/Downloads
create_perm_link $perm/gnupg $HOME/.gnupg
create_perm_link $perm/ssh $HOME/.ssh
create_perm_link $perm/zsh_history $HOME/.zsh_history
create_perm_link $perm/idea-config $HOME/.idea-config
