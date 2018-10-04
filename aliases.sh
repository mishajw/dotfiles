#!/bin/bash

# Add to .bashrc:
# source ~/scripts/aliases.sh

# Ubuntu
alias o="xdg-open"
alias ag="sudo apt-get"
alias ai="ag install"
alias as="apt-cache search"

# Arch
alias y="yaourt"
alias yn="y --noconfirm"
alias yu="y -Syyu ; echo 'UpdatesWidget' > $PANEL_FIFO"
alias yro="y -Rsn --noconfirm \$(y -Qdtq)"
alias df-packages="yaourt -Sy --needed --noconfirm $df/packages"

# Git
alias g="git"
gclone() {
  if [ -z $1 ]; then
    echo "Usage: $0 <github username>/<github repo>"
  fi

  git clone ssh://git@github.com/$1
}

make_git_aliases_global() {
  IFS=$'\n'

  for git_alias in $(git config --get-regexp alias); do
    final_alias=$(echo $git_alias | sed 's/alias.//g' | awk '{print $1;}')
    alias "g$final_alias"="git $final_alias"
  done
}

make_git_aliases_global

# SVN
alias va="svn add"
alias vu="svn update"
alias vc="svn commit -m"
alias vs="svn status"
alias vl="svn log"
alias vd="svn diff"

# ls
alias ls="exa --git"
alias ll="ls -l"
alias la="ls -la"

# Editing
alias e="vim"
alias se="EDITOR=vim sudoedit"

# VM
alias startcsecvm="VBoxManage startvm 'Intro to Computer Security' --type headless"
alias stopcsecvm="VBoxManage controlvm 'Intro to Computer Security' poweroff"

# Restart internet
alias resint="sudo systemctl restart NetworkManager.service"

# Browser
alias chrome="google-chrome-stable --force-device-scale-factor=1.2"

# Backup folder with date
backup() {
  if [ $# -lt 1 ]; then
    echo "Usage: $0 <file to backup> <optional -r>"
    return
  fi

  FILE_TO_BACKUP=$1
  REMOVE_ORIGINAL=false

  if [ "$2" = "-r" ]; then
    REMOVE_ORIGINAL=true
  fi

  DATE=$(date +"%Y%m%d_%H%M%S")

  if $REMOVE_ORIGINAL; then
    mv $FILE_TO_BACKUP ${FILE_TO_BACKUP}_$DATE
  else
    cp -r $FILE_TO_BACKUP ${FILE_TO_BACKUP}_$DATE
  fi
}

# Search in files
search() {
  if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <path> <search term>"
    return
  fi

  find $1 -type f | xargs grep -niEC 3 --color=always "$2" | less -R
}

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
display-start() {
  MODE_NAME="${SECOND_DISPLAY_X}x${SECOND_DISPLAY_Y}_${SECOND_DISPLAY_HZ}_3" 
  echo "Adding mode $MODE_NAME"
  xrandr --newmode $MODE_NAME `gtf $SECOND_DISPLAY_X $SECOND_DISPLAY_Y $SECOND_DISPLAY_HZ | grep Modeline | sed -E 's/Modeline "[^ ]*"//g'`
  xrandr --addmode $SECOND_DISPLAY $MODE_NAME
  xrandr --output $SECOND_DISPLAY --mode $MODE_NAME --above $MAIN_DISPLAY
  $cnf/bspwmrc
}

display-stop() {
  xrandr --output $SECOND_DISPLAY --off
  $cnf/bspwmrc
}

# Volume
set-vol() {
  if [ -z $1 ]; then exit; fi
  amixer sset $MASTER_SOUND ${1}% > /dev/null
  echo "VolumeWidget" > $PANEL_FIFO
}

# Networking
alias ip-pub="curl -s ipinfo.io | grep -oE '\"ip\": \"(.*)\"' | sed 's/\"ip\": //; s/\"//g'"

# Systemctl
alias sysstart="sudo systemctl start"
alias sysstop="sudo systemctl stop"
alias sysres="sudo systemctl restart"

# Python virtualenv
pf() {
  pip freeze | grep $1 >> requirements.txt
}

# Cargo
alias c="cargo"
alias cr="c run"
alias cb="c build"
alias ct="c test"
alias cf="c +nightly fmt"
alias cck="c check"

# sl
sl() {
  # Taken from: https://gir.st/blog/sl-alt.htm
  # sl - prints a mirror image of ls. (C) 2017 Tobias Girstmair, https://gir.st/, GPLv3
  LEN=$(ls "$@" | wc -L) # get the length of the longest line

  ls "$@" | rev | while read -r line
  do
    printf "%${LEN}.${LEN}s\\n" "$line" | sed 's/^\(\s\+\)\(\S\+\)/\2\1/'
  done
}

# Misc
alias dua="du -sh *"
csvview () { column -s, -t < $@ | less -#2 -N -S }
alias gourcec="gource -f -s 1 -a 1"
alias vnc="x11vnc -display :0"
alias net="slurm -i $NET"
cdmk () { mkdir -p -- "$1" && cd -P -- "$1" }
opr () { "$@" > /dev/null 2>&1 & disown }
alias dmenu="dmenu -o 0.8 -fn $MAIN_FONT -h 50 -w 500 -x 680 -y 490"
alias go-q="tmux attach -t quake"
alias sshuttlec="sshuttle --dns -r do 0/0"
alias xc="xclip -selection clipboard"
alias todo="vim ~/src/misc/todo.md"
alias py="python3 -i <(echo 'import numpy as np\nimport tensorflow as tf')"
alias pdf="opr evince"
alias cp="cp -r"
alias np='echo "$(nproc) * 1.5" | bc -l | grep --color=never -Po "^[^\.]*"'

