#!/usr/bin/env bash

battery_name=$(upower --enumerate | grep BAT)

if [ -z "$battery_name" ]; then
  percentage="N/A"
else
  percentage=$(
    upower --show-info $battery_name |
      grep percentage |
      grep -Po "[0-9]+"
  )
  if upower --show-info $battery_name |
    grep 'state:.*charging' >/dev/null; then
    percentage="+$percentage"
  fi
fi

echo "bat: $percentage"
