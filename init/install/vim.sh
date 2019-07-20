#!/usr/bin/env bash

set -o xtrace
set -e

git clone --depth 1 https://github.com/junegunn/fzf.git $HOME/.fzf
$HOME/.fzf/install

mkdir --parents ~/.vim/bundle
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
YCM=~/.vim/bundle/YouCompleteMe
vim +PluginInstall +qall
