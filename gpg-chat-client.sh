#!/bin/bash

nc -l -p 65000 | xargs -L1 -I{} bash -c 'base64 -d <(echo {}) | gpg --decrypt' 2> /dev/null
