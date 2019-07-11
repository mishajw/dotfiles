#!/usr/bin/env bash

pacman-install zsh oh-my-zsh

export ZSH=/usr/share/oh-my-zsh
export ZSH_PLUGINS=$ZSH/custom/plugins
export ZSH_SYNTAX=$ZSH_PLUGINS/zsh-syntax-highlighting
export ZSH_SUGGESTIONS=$ZSH_PLUGINS/zsh-autosuggestions
export ZSH_FZF=$ZSH_PLUGINS/fzf
export ZSH_FZF_PLUGIN=$ZSH_PLUGINS/fzf-zsh

if [[ ! -e "$ZSH_SYNTAX" ]]; then
  echo "Setting up syntax highlighting"
  sudo git clone \
    https://github.com/zsh-users/zsh-syntax-highlighting.git \
    $ZSH_SYNTAX
fi

if [[ ! -e "$ZSH_SUGGESTIONS" ]]; then
  echo "Setting up auto-suggestions"
  sudo git clone \
    https://github.com/zsh-users/zsh-autosuggestions \
    $ZSH_SUGGESTIONS
fi

if [[ ! -e "$ZSH_FZF" ]]; then
  echo "Setting up fzf"
  sudo git clone \
    https://github.com/junegunn/fzf.git \
    $ZSH_FZF
  sudo $ZSH_FZF/install --bin
fi

if [[ ! -e "$ZSH_FZF_PLUGIN" ]]; then
  echo "Setting up fzf plugin"
  sudo git clone \
    https://github.com/Treri/fzf-zsh.git \
    $ZSH_FZF_PLUGIN
fi
