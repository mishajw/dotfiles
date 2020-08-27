#!/usr/bin/env python

"""
Sets up monitors using xrandr.
"""

from subprocess import check_output, check_call
from typing import Iterator, List, Dict, Tuple
import sys


DESKTOPS_SOLO = [str(i) for i in range(1, 10)] + ["dmp"]
DESKTOPS_PRIMARY = [str(i) for i in range(1, 8)] + ["dmp"]
DESKTOPS_SECONDARY = ["a", "b"]


def main():
    monitors = set(get_connected_monitors())
    print("Connected monitors: " + ", ".join(monitors))

    if monitors == {"eDP1"}:
        run_xrandr(["--output eDP1 --primary --auto --scale 1x1", "--output DP1 --off"])
        set_desktops([("eDP1", DESKTOPS_SOLO)])
    elif monitors == {"screen"}:
        run_xrandr(["--output screen --primary --auto"])
        set_desktops([("screen", DESKTOPS_SOLO)])
    elif monitors == {"eDP1", "DP1"}:
        run_xrandr(
            ["--output DP1 --primary --auto", "--output eDP1 --same-as DP1 --scale-from 2560x1440"]
        )
        set_desktops([("eDP1", DESKTOPS_SOLO)])
        check_call(["bspc", "monitor", "DP1", "--remove"])
    elif monitors == {"eDP1", "HDMI1"}:
        run_xrandr(
            [
                "--output HDMI1 --primary --auto",
                "--output eDP1 --same-as HDMI1 --scale-from 1024x768",
            ]
        )
        set_desktops([("eDP1", DESKTOPS_SOLO)])
        check_call(["bspc", "monitor", "HDMI1", "--remove"])
    elif monitors == {"DP-0", "DP-2"}:
        run_xrandr(["--output DP-0 --primary --auto", "--output DP-2 --auto --left-of DP-0"])
        set_desktops([("DP-0", DESKTOPS_PRIMARY), ("DP-2", DESKTOPS_SECONDARY)])
    else:
        print("Unrecognized monitors")
        sys.exit(1)


def get_connected_monitors() -> Iterator[str]:
    for line in check_output(["xrandr"]).decode().split("\n"):
        split = line.split(" ")
        if len(split) < 2:
            continue
        monitor, status, *_ = split
        if status == "connected":
            yield monitor


def run_xrandr(commands: List[str]) -> None:
    for command in commands:
        print("Running: " + command)
        check_call(["xrandr", *command.split(" ")])


def set_desktops(monitor_desktops: List[Tuple[str, List[str]]]) -> None:
    monitors = [monitor for monitor, _ in monitor_desktops]
    print("Ordering monitors: " + ", ".join(monitors))
    check_call(["bspc", "wm", "--reorder-monitors", *monitors])

    for monitor, desktops in monitor_desktops:
        print(f"Setting desktops of {monitor}: {desktops}")
        check_call(["bspc", "monitor", monitor, "--reset-desktops", *desktops])


if __name__ == "__main__":
    main()
