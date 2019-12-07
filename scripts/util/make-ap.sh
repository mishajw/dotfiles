#!/usr/bin/env bash

if [[ $EUID -ne 0 ]]; then
  echo "Root required to make AP"
  exit 1
fi

rfkill unblock all
systemctl restart dhcpcd@enp0s25.service
create_ap -m bridge wlp4s0 enp0s25 mla-wifi mla-wifi -c 9
