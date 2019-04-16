#!/usr/bin/env bash
cd $df
shfmt -f . 2>&1 | xargs -I% shfmt -w -i 2 %
