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
alias yu="yn -Syua"

# Git
alias ga="git add"
alias gc="git commit -m"
alias gp="git push"
alias gpull="git pull --rebase"
alias gs="git status"
alias gd="git diff"
alias glog="git log --oneline"

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
alias e="nvim"
alias se="sudo nvim"

# VM
alias startcsecvm="VBoxManage startvm 'Intro to Computer Security' --type headless"
alias stopcsecvm="VBoxManage controlvm 'Intro to Computer Security' poweroff"

# Restart internet
alias resint="sudo systemctl restart NetworkManager.service"

# Mounts
mycloud () {
  if [ $# -eq 0 ]; then
    ip=$MYCLOUD_IP
  else
    ip=$1
  fi

  sudo mkdir -p /mnt/mycloud
  sudo mount -t cifs -o user=misha,passwd=,rw,file_mode=0777,dir_mode=0777 //$ip/misha /mnt/mycloud
}

# Displays
start-display() {
  xrandr --addmode $SECOND_DISPLAY $SECOND_DISPLAY_RES
  xrandr --output $SECOND_DISPLAY --mode $SECOND_DISPLAY_RES --above $MAIN_DISPLAY
  $cnf/bspwmrc
}

stop-display() {
  xrandr --output $SECOND_DISPLAY --off
  $cnf/bspwmrc
}

# Systemctl
alias sysstart="sudo systemctl start"
alias sysstop="sudo systemctl stop"
alias sysres="sudo systemctl restart"

# Misc
alias dua="du -sh *"
csvview () { column -s, -t < $@ | less -#2 -N -S }
alias gourcec="gource -f -s 1 -a 1"
alias vnc="x11vnc -display :0"
alias net="slurm -i $NET"

