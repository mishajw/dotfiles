#!/usr/bin/env bash

source $HOME/dotfiles/init/scripting.sh

source $init/modules/apt-get.sh
source $init/modules/brew.sh
source $init/modules/calc.sh
source $init/modules/exa.sh
source $init/modules/git.sh
source $init/modules/global-aliases.sh
source $init/modules/mac.sh
source $init/modules/make.sh
source $init/modules/python-interactive.sh
source $init/modules/quick.sh
source $init/modules/ssh.sh
source $init/modules/vim.sh

# Misc aliases and functions
alias res='exec /proc/$$/exe'
alias dua="du -sh *"
csvview() { column -s, -t <$@ | less -#2 -N -S; }
alias gourcec="gource -f -s 1 -a 1"
cdmk() { mkdir -p -- "$1" && cd -P -- "$1"; }
opr() {
  "$@" >/dev/null 2>&1 &
  disown
}
alias dmenu="dmenu -o 0.8 -fn $MAIN_FONT -h 50 -w 500 -x 680 -y 490"
alias sshuttlec="sshuttle --dns -r do 0/0"
alias xc="xclip -selection clipboard"
alias todo="vim ~/src/misc/todo.md"
alias py="python3 -i <(echo 'import numpy as np\nimport tensorflow as tf')"
alias pdf="opr evince"
alias cp="cp -r"
np() { nproc | awk "{print int(\$1 * ${1:-1.5})}"; }
alias ip-pub="curl -s ipinfo.io | grep -oE '\"ip\": \"(.*)\"' | sed 's/\"ip\": //; s/\"//g'"
pf() { pip freeze | grep $1 >>requirements.txt; }
wt() { while true; do $@; done; }
loop() { while true; do eval $@; done; }
alias ag="ag --pager less"

[ -f $local/interactive.sh ] && source $local/interactive.sh

# Start x if it isn't already started
pgrep X 1>/dev/null || ([ -z "$TMUX" ] && startx)

# Stop Ctrl+S/Q behaviour.
stty -ixon
