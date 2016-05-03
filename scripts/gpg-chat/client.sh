#!/usr/bin/env sh

if (($# != 3)); then
	echo "Usage: $0 <recipient> <server ip> <server port>"
	exit 1
fi

export REC=$1
cat | xargs -L1 -I{} bash -c 'gpg --encrypt -o- -r $REC <(echo {}) | base64 -w 0 ; echo' | /usr/bin/ncat "$2" "$3"
