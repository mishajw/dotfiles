#!/usr/bin/env bash
config="/etc/profile.d/jre.sh"
sudo su -c "echo export _JAVA_AWT_WM_NONREPARENTING=1 >> $config"
source $config
