#!/usr/bin/env zsh

source $HOME/dotfiles/init/scripting.sh

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

if [[ ! -e "$ANTIGEN_PATH" ]]; then
  echo "Antigen not installed, plugins unavailable"
else
  source $ANTIGEN_PATH
  antigen use oh-my-zsh
  antigen bundle sudo
  antigen bundle command-not-found
  antigen bundle fzf-zsh
  antigen bundle zsh-users/zsh-syntax-highlighting
  antigen bundle zsh-users/zsh-autosuggestions
  antigen theme garyblessington
  antigen apply
fi

FZF_KEY_BINDINGS=$HOME/.fzf/shell/key-bindings.zsh
if [[ -e $FZF_KEY_BINDINGS ]]; then
  source $FZF_KEY_BINDINGS
fi

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

source $HOME/dotfiles/init/interactive.sh
