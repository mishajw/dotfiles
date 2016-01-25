#!/bin/bash

# Add to .bashrc:
# source ~/scripts/aliases.sh

# Ubuntu
alias o="xdg-open"
alias ag="sudo apt-get install"
alias acs="apt-cache search"

# Arch
alias y="yaourt"
alias yn="y --noconfirm"

# Git
alias ga="git add"
alias gc="git commit -m"
alias gp="git push"
alias gpull="git stash ; git fetch ; git rebase FETCH_HEAD"
alias gs="git status"
alias gd="git diff"

# ls
alias ll="ls -lah"
alias la="ls -a"

# Editing
alias e="gvim"
alias se="sudo gvim"
alias te="vim"
alias ste="sudo vim"

# VM
alias startcsecvm="VBoxManage startvm 'Intro to Computer Security' --type headless"
alias stopcsecvm="VBoxManage controlvm 'Intro to Computer Security' poweroff"

# Restart internet
alias resint="sudo systemctl restart NetworkManager.service"


