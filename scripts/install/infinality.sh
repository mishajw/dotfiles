#!/bin/bash

pacman-key --recv-keys AE6866C7962DDE58 962DDE58
pacman-key --lsign-key 962DDE58
echo -e "[infinality-bundle]\nServer = http://bohoomil.com/repo/\$arch" >> /etc/pacman.conf
echo -e "[multilib]\nInclude = /etc/pacman.d/mirrorlist" >> /etc/pacman.conf
sudo pacman -Syyu
sudo pacman -S infinality-bundle
sudo pacman-key --refresh-keys

