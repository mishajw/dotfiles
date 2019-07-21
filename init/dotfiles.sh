#!/usr/bin/env bash

set -o xtrace
set -e

CLONE_PATH=$HOME/.local-perm
DF_PATH=$CLONE_PATH/dotfiles
REPO_HTTPS='https://github.com/mishajw/dotfiles.git'
REPO_SSH='git@github.com:mishajw/dotfiles.git'

[[ "$USER" != "root" ]] || exit 1
command -v git 1>/dev/null || exit 1
command -v zsh 1>/dev/null || exit 1
command -v python 1>/dev/null || exit 1

if [[ ! -e $DF_PATH ]]; then
  echo "Cloning dotfiles"
  mkdir -p $CLONE_PATH
  git clone $REPO_HTTPS $DF_PATH
fi

lperm=$HOME/.local-perm perm=$HOME/.perm $DF_PATH/init/perm.sh

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
