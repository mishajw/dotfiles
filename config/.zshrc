#!/usr/bin/env zsh

export ZSH=$HOME/.oh-my-zsh

# ZSH theme
ZSH_THEME="garyblessington"
# - and _ wont matter in completion
HYPHEN_INSENSITIVE="true"
# Command auto-correction.
ENABLE_CORRECTION="true"
# Red dots when waiting for completion
COMPLETION_WAITING_DOTS="true"
# Makes checking using large repos faster
DISABLE_UNTRACKED_FILES_DIRTY="true"
# Change timestamps
HIST_STAMPS="yyyy-mm-dd"
# Turn off autocorrect
unsetopt correct_all
# TODO: Is this needed?
export PATH="$PATH:\
  /usr/local/sbin:\
  /usr/local/bin:\
  /usr/bin:\
  /usr/lib/jvm/default/bin:\
  /usr/bin/site_perl:\
  /usr/bin/vendor_perl:\
  /usr/bin/core_perl"
# Word navigation
bindkey "^[[1;3C" forward-word
bindkey "^[[1;3D" backward-word
# jk to scroll through history
bindkey "^[j" history-beginning-search-forward
bindkey "^[k" history-beginning-search-backward

# Load oh-my-zsh
plugins=(sudo zsh-syntax-highlighting zsh-autosuggestions fzf-zsh)
source $ZSH/oh-my-zsh.sh
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

source $HOME/dotfiles/init/interactive.sh
