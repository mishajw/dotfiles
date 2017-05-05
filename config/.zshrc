# Path to your oh-my-zsh installation.
export ZSH=$HOME/.oh-my-zsh

# ZSH theme
ZSH_THEME="bira"

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

# Plugins list
plugins=(sudo zsh-syntax-highlighting zsh-autosuggestions)

export PATH="$PATH:\
  /usr/local/sbin:\
  /usr/local/bin:\
  /usr/bin:\
  /usr/lib/jvm/default/bin:\
  /usr/bin/site_perl:\
  /usr/bin/vendor_perl:\
  /usr/bin/core_perl"

# Load oh-my-zsh
source $ZSH/oh-my-zsh.sh

# Set language
export LANG=en_GB.UTF-8

# Word navigation
bindkey "^[[1;3C" forward-word
bindkey "^[[1;3D" backward-word

# Turn off autocorrect
unsetopt correct_all

# J&K to scroll through history
bindkey "^[j" history-beginning-search-forward
bindkey "^[k" history-beginning-search-backward

# Set autosuggest colour
export ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE="fg=3"

source $HOME/dotfiles/scripts/start/shell.sh

