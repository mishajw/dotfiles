#!/usr/bin/env bash

alias g="git"
{
  git config --get-regexp alias | while read git_alias; do
    final_alias=$(echo $git_alias | sed 's/alias.//g' | awk '{print $1;}')
    alias "g$final_alias"="git $final_alias"
  done
}
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

function gc() { git commit --message "$*"; }
function gca() { git commit --all --message "$*"; }
function gcf() { git log --oneline --author Misha | fzf | awk '{print $1}' | xargs -I% git commit --fixup %; }
function gcl() { git clone ssh://git@github.com/$*; }
function gbl() { git branch --list | fzf | sed 's/\\*//g' | xargs git checkout; }

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

alias -g Gc="\$(\
  git log --oneline --author \$(git config user.email) \
  | fzf \
  | awk '{print \$1}')"
alias -g Gb="\$(git branch | fzf | sed 's/*//g')"
