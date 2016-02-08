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

# SVN
alias va="svn add"
alias vu="svn update"
alias vc="svn commit -m"
alias vs="svn status"
alias vl="svn log"
alias vd="svn diff"

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

# Systemctl
alias sysstart="sudo systemctl start"
alias sysstop="sudo systemctl stop"
alias sysres="sudo systemctl restart"

# Misc
alias dua="du -sh *"
csvview () { column -s, -t < $@ | less -#2 -N -S }

