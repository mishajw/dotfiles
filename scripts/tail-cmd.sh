#!/usr/bin/env bash

# Needed to disown main job.
set -m
# Pass output through LOG so that Ctrl-C in less (to exit +F) doesn't kill main
# job.
LOG=$(mktemp)
"$@" > $LOG 2>&1 &
# Record PID, disown so it doens't get killed by Ctrl-C.
SPAWNED_PID=$!
disown
# Kill PID when shell exits.
trap "kill -- -$SPAWNED_PID" EXIT
# Start less to observe output.
less +F $LOG
