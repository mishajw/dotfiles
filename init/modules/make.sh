#!/usr/bin/env bash

m() {
    if [ -f Makefile ]; then
        make $@
    elif [ -f package.json ]; then
        npm run $@
    elif [ -f poetry.lock ]; then
        poetry run $@
    else
        make $@
    fi
}
