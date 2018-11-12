#!/usr/bin/env bash

alias g="git"
{
  IFS=$'\n'

  for git_alias in $(git config --get-regexp alias); do
    final_alias=$(echo $git_alias | sed 's/alias.//g' | awk '{print $1;}')
    alias "g$final_alias"="git $final_alias"
  done
}
