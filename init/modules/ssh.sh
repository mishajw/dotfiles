function dfssh() {
  if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <ssh target> <tmux name> <command...>"
    return -1
  fi
  SSH_TARGET="$1"
  SESSION_NAME="$2"
  COMMAND="${@:3}"

  while true; do
    ssh -L 8888:localhost:8888 -t "$SSH_TARGET" -- tmux new-session -A -s "$SESSION_NAME" $COMMAND
    echo "Session terminated"
    echo "- SSH target: $SSH_TARGET"
    echo "- Session name: $SESSION_NAME"
    echo "- Command: $COMMAND"
    read "?Press enter to reconnect, Ctrl-C to terminate"
  done
}

function dfssh-first() {
  SSH_TARGET=$(cat ~/.ssh/config | awk '$1 == "Host" {print $2}' | head -1)
  dfssh $SSH_TARGET "${@}"
}

function dfssh-first-random() {
  SESSION_NAME=$(cat /etc/dictionaries-common/words | grep -P '^[a-z]{3,8}$' | shuf -n 1)
  dfssh-first "$SESSION_NAME" "${@}"
}

alias s="dfssh-first-random"
alias sn="dfssh-first"

