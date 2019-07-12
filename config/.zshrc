#!/usr/bin/env zsh

source $HOME/dotfiles/init/interactive.sh

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

# Load oh-my-zsh
plugins=(sudo zsh-syntax-highlighting zsh-autosuggestions fzf-zsh)
source $OH_MY_ZSH/oh-my-zsh.sh

# Turn off autocorrect
unsetopt correct_all

# Word navigation
bindkey "^[l" forward-word
bindkey "^[h" backward-word
# M-jk to scroll through history
bindkey "^[j" history-beginning-search-forward
bindkey "^[k" history-beginning-search-backward

# This speeds up pasting w/ autosuggest
# https://github.com/zsh-users/zsh-autosuggestions/issues/238
pasteinit() {
  OLD_SELF_INSERT=${${(s.:.)widgets[self-insert]}[2,3]}
  zle -N self-insert url-quote-magic # I wonder if you'd need `.url-quote-magic`?
}
pastefinish() {
  zle -N self-insert $OLD_SELF_INSERT
}
zstyle :bracketed-paste-magic paste-init pasteinit
zstyle :bracketed-paste-magic paste-finish pastefinish
