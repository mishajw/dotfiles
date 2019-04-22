#!/usr/bin/env bash

IP_INFO=$(ip address show dev $IP_DEVICE)
if echo "$IP_INFO" | grep 'DOWN' > /dev/null; then
  echo "discon"
  exit
fi

IP=$(
  echo "$IP_INFO" |
    grep -P '\binet\b' |
    tail -1 | awk '{print $2}' |
    sed 's/\/[0-9]*$//')
if [ -z $IP ]; then
  echo "no ip"
  exit
fi

echo $IP
