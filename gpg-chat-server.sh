#!/bin/bash

cat | xargs -L1 -I{} bash -c 'gpg --encrypt -o- -r $1 <(echo {}) | base64 -w 0 ; echo' | nc $2 $3
