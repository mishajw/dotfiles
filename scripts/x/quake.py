#!/usr/bin/env python

"""
Toggle a drop-down terminal using termite and xdotool
"""

from subprocess import run, Popen, DEVNULL, PIPE, check_output
from typing import Optional, Tuple
import argparse
import os
import re
import time
import logging
from collections import namedtuple

LOG = logging.getLogger(__name__)
CLASS_NAME = "quake"
DISPLAY = os.environ["DISPLAY"]

LocationConfig = namedtuple(
    "LocationConfig", ["side", "percent", "padding", "edge_distance", "border"]
)


def main(tag: str, command: str, window_id_directory: str, location: LocationConfig):
    if not os.path.isdir(window_id_directory):
        LOG.debug("Creating directory to store window IDs")
        os.makedirs(window_id_directory)

    # Get the window ID, creating the window if it doesn't exist
    window_id = get_window_id(tag, window_id_directory)
    is_new_window = False
    if not window_id or not is_window_alive(window_id):
        LOG.info("Creating windows")
        window_id = create_window(command)
        is_new_window = True
        store_window_id(window_id, tag, window_id_directory)
    if is_window_visible(window_id):
        if not is_window_focused(window_id):
            focus_window(window_id)
        elif not is_new_window:
            LOG.info("Making window invisible")
            set_window_visible(window_id, False)
    else:
        set_window_geom(window_id, location)
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


def get_active_window_id() -> Optional[int]:
    output = run(["xdotool", "getactivewindow"], stdout=PIPE)
    if output.returncode != 0:
        return None
    return int(output.stdout.decode())


def is_window_visible(window_id: int) -> bool:
    visible_windows = (
        check_output(["xdotool", "search", "--onlyvisible", ".*"]).decode().split("\n")
    )
    return str(window_id) in visible_windows


def set_window_visible(window_id: int, visible: bool):
    LOG.info("Setting window visible to %s", visible)
    if visible:
        check_output(["xdotool", "windowmap", str(window_id)])
    else:
        check_output(["xdotool", "windowunmap", str(window_id)])


def set_window_geom(window_id: int, location: LocationConfig):
    set_window_floating(window_id)
    desktop_width, desktop_height, desktop_x, desktop_y = get_desktop_geometry()
    LOG.debug("Found desktop size of %d, %d", desktop_width, desktop_height)

    if location.side == "top" or location.side == "bottom":
        window_width = desktop_width - location.border * 2 - location.padding * 2
        window_height = int(desktop_height * location.percent)
    else:
        window_width = int(desktop_width * location.percent)
        window_height = desktop_height - location.border * 2 - location.padding * 2
    LOG.debug("Setting window size to %d, %d", window_width, window_height)

    # TODO: Can we simplify this?
    if location.side == "top":
        window_x = desktop_x + location.padding
        window_y = desktop_y + location.edge_distance
    elif location.side == "left":
        window_x = desktop_x + location.edge_distance
        window_y = desktop_y + location.padding
    elif location.side == "bottom":
        window_x = desktop_x + location.padding
        window_y = (
            desktop_y + desktop_height - window_height - location.border - location.edge_distance
        )
    elif location.side == "right":
        window_x = (
            desktop_x + desktop_width - window_width - location.border - location.edge_distance
        )
        window_y = desktop_y + location.padding
    LOG.debug("Setting window location to %d, %d", window_x, window_y)

    # Fix strange issue with y=0 making window appear in middle of screen
    if window_y == 0:
        window_y = 1

    check_output(["xdotool", "windowmove", str(window_id), str(window_x), str(window_y)])
    check_output(
        ["xdotool", "windowsize", str(window_id), str(window_width), str(window_height),]
    )


def set_window_floating(window_id: int):
    LOG.debug("Setting window classname to %s", CLASS_NAME)
    check_output(["xdotool", "set_window", "--classname", CLASS_NAME, str(window_id)])

    rules = check_output(["bspc", "rule", "--list"]).decode()
    if CLASS_NAME not in rules:
        LOG.debug("Adding BSPWM rule to float classnmae")
        check_output(
            ["bspc", "rule", "--add", "*:" + CLASS_NAME, "state=floating", "sticky=on",]
        )


def get_desktop_geometry() -> Tuple[int, int]:
    xrandr_geometry_regex = re.compile(r"(\d+)x(\d+)\+(\d+)\+(\d+)")
    focused_x, focused_y = get_focused_location()

    for line in check_output(["xrandr"]).decode().split("\n"):
        if " connected " not in line:
            continue

        match = xrandr_geometry_regex.search(line)
        if match is None:
            continue

        size_x = int(match.group(1))
        size_y = int(match.group(2))
        offset_x = int(match.group(3))
        offset_y = int(match.group(4))

        if offset_x <= focused_x < offset_x + size_x and offset_y <= focused_y < offset_y + size_y:
            return size_x, size_y, offset_x, offset_y

    raise AssertionError("No matching monitor found")


def get_focused_location() -> Tuple[int, int]:
    xdotool_position_regex = re.compile(r"Position: (\d+),(\d+)")
    xdotool_mouse_regex = re.compile(r"x\:(\d+) y\:(\d+)")
    window_id = get_active_window_id()
    if window_id is not None:
        window_geometry_str = check_output(
            ["xdotool", "getwindowgeometry", str(window_id)]
        ).decode()
        match = xdotool_position_regex.search(window_geometry_str)
        assert match is not None
        return int(match.group(1)), int(match.group(2))
    else:
        # If we can't find the active window, return mouse location
        mouse_str = check_output(["xdotool", "getmouselocation"]).decode()
        match = xdotool_mouse_regex.search(mouse_str)
        assert match is not None
        return int(match.group(1)), int(match.group(2))


def is_window_focused(window_id: int) -> bool:
    focused_id = check_output(["xdotool", "getwindowfocus"]).decode().strip()
    return int(focused_id) == window_id


def focus_window(window_id: int):
    focused_id = check_output(["xdotool", "windowactivate", str(window_id)])


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

    # Set up command line arguments
    parser = argparse.ArgumentParser("quake")
    parser.add_argument("--tag", type=str, required=True)
    parser.add_argument("--command", type=str, required=True)
    parser.add_argument("--window-id-directory", type=str, default="/tmp/quake-window-ids")
    parser.add_argument("--side", choices=["top", "bottom", "left", "right"], default="top")
    parser.add_argument("--percent", type=float, default=0.3)
    parser.add_argument("--padding", type=int, default=20)
    parser.add_argument("--edge-distance", type=int, default=0)
    parser.add_argument("--border", type=int, default=0)
    args = parser.parse_args()

    main(
        args.tag,
        args.command,
        args.window_id_directory,
        LocationConfig(args.side, args.percent, args.padding, args.edge_distance, args.border,),
    )
