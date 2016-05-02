#!/bin/bash

cat | xargs -L1 -I{} bash -c 'gpg --encrypt -o- -r mishajw@gmail.com <(echo {}) | base64 -w 0 ; echo' | nc localhost 65000
