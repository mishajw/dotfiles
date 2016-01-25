#!/bin/bash

sudo mkdir -p /mnt/sshfsrpi

sudo sshfs -o allow_other pi@192.168.0.126:/home/pi /mnt/sshfsrpi

