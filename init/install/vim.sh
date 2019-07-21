#!/usr/bin/env bash

set -o xtrace
set -e

if [[ ! -e $HOME/.fzf ]]; then
  git clone --depth 1 https://github.com/junegunn/fzf.git $HOME/.fzf
  $HOME/.fzf/install
fi

if [[ ! -e $HOME/.vim/bundle ]]; then
  mkdir --parents ~/.vim/bundle
  git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
  YCM=~/.vim/bundle/YouCompleteMe
fi
vim +PluginInstall +qall
