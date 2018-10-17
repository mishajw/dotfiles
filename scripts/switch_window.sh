#!/bin/zsh

source $df/aliases.sh
echo $(alias dmenu) >> /tmp/test

bspc node -f $(bspc query -N | xargs -I^ bash -c 'echo -n "^: " ; xtitle ^ ' | dmenu | sed 's/\:.*//g')

