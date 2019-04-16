#!/usr/bin/env bash

MYCLOUD_IP=192.168.1.218
MYCLOUD_DIRECTORY=/mnt/mycloud

mycloud() {
  echo Mounting mycloud at $MYCLOUD_IP at $MYCLOUD_DIRECTORY
  mkdir -p $MYCLOUD_DIRECTORY
  sudo mount --types cifs \
    --options user=misha,rw,file_mode=0777,dir_mode=0777,uid=$(id -u),gid=$(id -g) \
    //$MYCLOUD_IP/misha $MYCLOUD_DIRECTORY
}
