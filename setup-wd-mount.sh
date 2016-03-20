#!/bin/bash

sudo mkdir -p /mnt/mycloud

sudo mount -t cifs -o user=misha,passwd=,rw,file_mode=0777,dir_mode=0777 //192.168.0.22/misha /mnt/mycloud

