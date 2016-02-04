#!/bin/bash

source $PANEL_PATH/widgets/panelParams.py

while true; do
  if [[ "$(ip addr show dev wlp4s0 | grep DOWN)" ]]; then
    echo -e '\uf119'
  else
    ip addr show dev wlp4s0 | grep 'inet ' | awk '{print $2}' | awk -F '/' '{print "%{A:urxvt -e bash -c \"sudo systemctl restart NetworkManager.service\":}" $1 "%{A}"}'
  fi

  sleep $SLEEP_IPADDR
done

