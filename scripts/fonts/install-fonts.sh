#!/usr/bin/env bash

all_packages=""

while read font_line; do
  font_package=$(echo $font_line | awk '{print $1;}')
  all_packages="$all_packages $font_package"
done <font-list

echo $all_packages

yaourt -S $all_packages
