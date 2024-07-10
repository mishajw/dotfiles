#!/usr/bin/env bash

# ROOT=$(dirname $(pwd)/${(%):-%N})
ROOT=$(dirname ${(%):-%N})
_log() {
  echo -e "[\033[32m"mishajw/dotfiles"\033[39m]" $@
}
_log "setting up shell ($ROOT)"

# env
export LANG=en_GB.UTF-8
export LANGUAGE="$LANG"
export LC_ALL="$LANG"

# globals
alias -g G='| grep'
alias -g Gi='| grep -i'
alias -g L="| less"
alias -g C="| wc -l"
alias -g Se="2>&1"
alias -g Ps="\$(ps -axo 'pid args' | awk 'NR!=1' | fzf | awk '{print \$1}')"

# apt-get
alias aget="sudo apt-get"
alias ai="aget install"
alias as="apt-cache search"

# brew
[ -e /opt/homebrew/bin/brew ] 1>/dev/null && eval "$(/opt/homebrew/bin/brew shellenv)"
alias b="brew"
alias bi="brew install"
alias bf="brew bundle --file ~/dotfiles/config/Brewfile dump -f"

# calc
_calc() {
  if [[ "$#" == "0" ]]; then
    echo "Usage: $0 <maths>"
    return 1
  fi
  MATHS="$@"
  python -c "from math import *; print($MATHS)"
}
alias calc="noglob py-calc"

# exa
if command -v exa 1>/dev/null; then
  alias ls="exa --color=always"
  alias ll="ls -l"
  alias la="ls -la"
  alias lt="ls -T"
fi

# git
alias g="git"
alias ga='git add'
alias gap='git add --patch'
alias gb='git branch'
alias gcam='git commit --amend'
alias gco='git checkout'
alias gd='git diff'
alias gds='git diff --staged'
alias gf='git fetch'
alias gl='git log --oneline --decorate'
alias glg='git log --oneline --decorate --graph'
alias gm='git merge'
alias gp='git push'
alias gpf='git push --force'
alias gpl='git pull'
alias gpsup='git push --set-upstream origin $(git_current_branch)'
alias grao='git remote add origin'
alias grb='git rebase --interactive --autosquash'
alias grba='git rebase --abort'
alias grbc='git rebase --continue'
alias grbh='git rebase --interactive HEAD~20'
alias gs='git status'
alias gsh='git show'
alias gshf='git show --name-only'
alias gsi='git submodule init'
alias gst='git stash'
alias gstd='git stash drop'
alias gstn='git stash push --message'
alias gstp='git stash pop'
alias gstsh='git stash show --patch'
alias gsu='git submodule update'
function gc() { git commit --message "$*"; }
function gca() { git commit --all --message "$*"; }
function gcf() { git log --oneline --author Misha | fzf | awk '{print $1}' | xargs -I% git commit --fixup %; }
function gcl() { git clone ssh://git@github.com/$*; }
function gbl() { git branch --list | fzf | sed 's/\\*//g' | xargs git checkout; }
g-rm-branch() {
  current_branch=$(git rev-parse --abbrev-ref HEAD)
  if ! git branch | grep -q "main"; then
    echo "No main branch"
    return 0
  fi
  if [[ "$current_branch" == "main" ]]; then
    echo "Can't delete main branch"
    return 0
  fi

  echo "Deleting branch $current_branch"
  git checkout main \
    && git branch -D $current_branch

  if git branch --all | grep -q "origin/$current_branch"; then
    echo "Deleting remote branch $current_branch"
    git push origin --delete $current_branch
  fi
}
alias -g Gc="\$(\
  git log --oneline --author \$(git config user.email) \
  | fzf \
  | awk '{print \$1}')"
alias -g Gb="\$(git branch | fzf | sed 's/*//g')"

# mac key overrides
if [ "$(uname)" != "Darwin" ]; then
    bindkey "∆" history-beginning-search-forward
    bindkey "˚" history-beginning-search-backward
    bindkey "¬" forward-word
    bindkey "˙" backward-word
fi

# make
m() {
    if [ -f Makefile ]; then
        make $@
    elif [ -f package.json ]; then
        npm run $@
    elif [ -f poetry.lock ]; then
        poetry run $@
    else
        make $@
    fi
}

# pyenv
if command -v pyenv 1>/dev/null 2>&1; then
  eval "$(pyenv init --path)"
  eval "$(pyenv init -)"
  alias python="python3"
fi

# editors
export EDITOR="vim"
alias e="vim"
alias se="EDITOR=vim sudoedit"

# theme
setopt PROMPT_SUBST
PROMPT='%F{cyan}%c%f %F{red}${vcs_info_msg_0_}%f$ '

# misc
cdmk() { mkdir -p -- "$1" && cd -P -- "$1"; }
alias ".."="cd .."
alias reup="source ~/.zshrc"

[ -f $ROOT/local.sh ] && source $ROOT/local.sh
_log done
