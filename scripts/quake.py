#!/usr/bin/env python

"""
Toggle a drop-down terminal using termite and xdotool
"""

from subprocess import run, call, Popen, DEVNULL, PIPE
import time
import os
import argparse
from typing import Optional

CLASS_NAME = "quake"
DISPLAY = os.environ["DISPLAY"]

def main(tag: str, command: str, window_id_directory: str):
    if not os.path.isdir(window_id_directory):
        os.makedirs(window_id_directory)

    # Get the window ID, creating the window if it doesn't exist
    window_id = get_window_id(tag, window_id_directory)
    is_new_window = False
    if not window_id or not is_window_alive(window_id):
        print("Creating windows")
        window_id = create_window(command)
        is_new_window = True
        store_window_id(window_id, tag, window_id_directory)
    if is_window_visible(window_id) and not is_new_window:
        print("Making window invisible")
        set_window_visible(window_id, False)
    else:
        print("Making window visible")
        set_window_geom(window_id)
        set_window_visible(window_id, True)

def get_window_id(tag: str, window_id_directory: str) -> Optional[int]:
    window_id_path = os.path.join(window_id_directory, tag + DISPLAY)
    if not os.path.isfile(window_id_path):
        return None
    with open(window_id_path, "r") as f:
        return int(next(f))

def store_window_id(window_id: int, tag: str, window_id_directory: str):
    window_id_path = os.path.join(window_id_directory, tag + DISPLAY)
    with open(window_id_path, "w") as f:
        f.write(str(window_id))

def is_window_alive(window_id: int) -> bool:
    return run(["xdotool", "getwindowname", str(window_id)]).returncode == 0

def create_window(command: str) -> int:
    previous = get_active_window_id()
    Popen(command.split(" "))
    while True:
        current = get_active_window_id()
        if current != previous:
            set_window_visible(current, False)
            return current

def get_active_window_id() -> int:
    return int(run(
        ["xdotool", "getactivewindow"],
        stdout=PIPE).stdout.decode())

def is_window_visible(window_id: int) -> bool:
    visible_windows = run(
        ["xdotool", "search", "--onlyvisible", ".*"],
        stdout=PIPE).stdout.decode().split("\n")
    return str(window_id) in visible_windows

def set_window_visible(window_id: int, visible: bool):
    if visible:
        run(["xdotool", "windowmap", str(window_id)]);
    else:
        run(["xdotool", "windowunmap", str(window_id)]);

def set_window_geom(window_id: int):
    height = os.environ["PANEL_HEIGHT"]
    run(
        ["xdotool", "set_window", "--classname", CLASS_NAME, str(window_id)],
        check=True)
    run(["bspc", "rule", "--add", "*:" + CLASS_NAME,
        "state=floating", "sticky=on", "border=on"], check=True)
    run(
        ["xdotool", "windowmove", str(window_id), "0", height],
        check=True)
    run(["xdotool", "windowsize", str(window_id), "2556", "400"], check=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser("quake")
    parser.add_argument("--tag", type=str, required=True)
    parser.add_argument("--command", type=str, required=True)
    parser.add_argument("--window-id-directory", type=str,
        default="/tmp/quake-window-ids")
    args = parser.parse_args()

    main(args.tag, args.command, args.window_id_directory)
