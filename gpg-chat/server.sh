#!/usr/bin/env sh

if (($# != 1)); then
	echo "Usage: $0 <port>"
	exit 1
fi

/usr/bin/ncat -kl -p $1 | xargs -L1 -I{} bash -c 'base64 -d <(echo {}) | gpg --decrypt'
