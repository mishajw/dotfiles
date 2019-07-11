#!/usr/bin/env bash

ZSH_CUSTOM=${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}
if [[ -e "$ZSH_CUSTOM" ]]; then
  exit
fi

# Get oh my zsh
sh -c "$(curl -fsSL \
  https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

# Set up syntax highlighting
git clone \
  https://github.com/zsh-users/zsh-syntax-highlighting.git \
  ${ZSH_CUSTOM}/plugins/zsh-syntax-highlighting

# Set up auto-suggestions
git clone \
  https://github.com/zsh-users/zsh-autosuggestions \
  ${ZSH_CUSTOM}/plugins/zsh-autosuggestions
