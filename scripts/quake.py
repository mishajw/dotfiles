#!/usr/bin/env python3

"""
Toggle a drop-down terminal using termite and xdotool
"""

from subprocess import run, Popen
import time
import os

TERMINAL_NAME = "QuakeTerminal"
XDO_CMD = [
    "xdotool", "search",
    ]

# Try to hide the terminal
hide_result = run(XDO_CMD + [
    "--onlyvisible", "--classname", TERMINAL_NAME, "windowunmap"])
if hide_result.returncode == 0:
    exit()

# If we couldn't hide, then the terminal is already hidden, so we should show
# the terminal
show_result = run(XDO_CMD + ["--classname", TERMINAL_NAME, "windowmap"])
if show_result.returncode == 0:
    exit()

# If we couldn't show, then the terminal must not exist, so we should create it
Popen([
    "termite",
    "--name", TERMINAL_NAME,
    "--exec", "tmux new -s quake"])
time.sleep(0.1)
# Set position and size of terminal
run(XDO_CMD + [
    "--classname", TERMINAL_NAME,
    "windowmove", "0", os.environ["PANEL_HEIGHT"]], check=True)
run(XDO_CMD + [
    "--classname", TERMINAL_NAME,
    "windowsize", "2556", "400"], check=True)
