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
alias yu="yn -Syua ; echo 'UpdatesWidget' > $PANEL_FIFO"
alias yro="y -Rsn --noconfirm \(y -Qdtq\)"
alias df-packages="yaourt -Sy --needed --noconfirm $df/packages"

# Git
alias g="git"
function gclone
  if test -z $1
    echo "Usage: $0 <github username>/<github repo>"
  end

  git clone ssh://git@github.com/$1
end

function make_git_aliases_global
  # IFS=$'\n'

  for git_alias in (git config --get-regexp alias)
    set final_alias (echo $git_alias | sed 's/alias./g/g')
    set alias_name (echo $final_alias | awk '{print $1;}')
    set alias_command (echo $final_alias | awk '{$1=""; print $0;}')
    alias "$alias_name"="git$alias_command"
    echo "$alias_command"
  end
end

make_git_aliases_global

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
alias e=vim
# alias se="sudo nvim"

# VM
alias startcsecvm="VBoxManage startvm 'Intro to Computer Security' --type headless"
alias stopcsecvm="VBoxManage controlvm 'Intro to Computer Security' poweroff"

# Restart internet
alias resint="sudo systemctl restart NetworkManager.service"

# Search in files
function search
  if test (count $argv) -ne 2; then
    echo "Usage: $0 <path> <search term>"
    return
  end

  find $1 -type f | xargs grep -iEC 3 --color=always "$2" | less -R
end

# Mounts
function mycloud
  bash -e '
    if [ $# -eq 0 ]; then
      ip=$MYCLOUD_IP
    else
      ip=$1
    fi

    sudo mkdir -p /mnt/mycloud
    sudo mount -t cifs -o user=misha,passwd=,rw,file_mode=0777,dir_mode=0777 //$ip/misha /mnt/mycloud
  '
end

# Displays
function display-start
  xrandr --addmode $SECOND_DISPLAY $SECOND_DISPLAY_RES
  xrandr --output $SECOND_DISPLAY --mode $SECOND_DISPLAY_RES --above $MAIN_DISPLAY
  $cnf/bspwmrc
end

function display-stop
  xrandr --output $SECOND_DISPLAY --off
  $cnf/bspwmrc
end

# Volume
function set-vol
  bash -e '
    if [ -z $1 ]; then return; fi
    amixer sset $MASTER_SOUND ${1}% > /dev/null
    echo "VolumeWidget" > $PANEL_FIFO
  '
end

# Networking
alias ip-pub="curl -s ipinfo.io | grep -oE '\"ip\": \"(.*)\"' | sed 's/\"ip\": //; s/\"//g'"

# Systemctl
alias sysstart="sudo systemctl start"
alias sysstop="sudo systemctl stop"
alias sysres="sudo systemctl restart"

# Misc
alias dua="du -sh *"
function csvview; column -s, -t < $@ | less -#2 -N -S; end
alias gourcec="gource -f -s 1 -a 1"
alias vnc="x11vnc -display :0"
alias net="slurm -i $NET"
function cdmk; mkdir -p -- "$1"; and cd -P -- "$1"; end
function opr; $argv > /dev/null 2>&1 & disown; end
alias dmenu="dmenu -o 0.8 -fn $MAIN_FONT -h 50 -w 500 -x 680 -y 490"
alias go-q="tmux attach -t quake"
alias sshuttlec="sshuttle --dns -r do 0/0"

