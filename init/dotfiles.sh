#!/usr/bin/env bash

set -o xtrace
set -e

DF_PATH=$HOME/dotfiles
REPO_HTTPS='https://github.com/mishajw/dotfiles.git'
REPO_SSH='git@github.com:mishajw/dotfiles.git'

[[ "$USER" != "root" ]] || exit 1

sudo pacman -S git zsh python --noconfirm --needed

if [[ ! -e $DF_PATH ]]; then
  echo "Cloning dotfiles"
  git clone $REPO_HTTPS $DF_PATH
fi

cd $DF_PATH
git remote set-url origin $REPO_HTTP \
  && git fetch \
  && git remote set-url origin $REPO_SSH
git checkout master

source $HOME/dotfiles/init/scripting.sh

echo "Setting up yay"
$init/install/yay.sh
echo "Setting up python"
$init/install/python.sh
echo "Setting up zsh"
$init/install/zsh.sh

echo "Setting up config files"
$DF_PYTHON $scr/make-symlinks.py
