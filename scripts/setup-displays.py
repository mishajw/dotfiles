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
        run_xrandr(["--output eDP1 --primary --auto"])
        set_desktops([("eDP1", DESKTOPS_SOLO)])
    elif monitors == {"eDP1", "DP1"}:
        run_xrandr(["--output DP1 --primary --auto", "--output eDP1 --off"])
        set_desktops([("DP1", DESKTOPS_SOLO)])
    elif monitors == {"DP-2", "DP-0"}:
        run_xrandr([
            "--output DP-2 --primary --auto",
            "--output DP-0 --auto --left-of DP-2 --rotate left",
        ])
        set_desktops([("DP-2", DESKTOPS_PRIMARY), ("DP-0", DESKTOPS_SECONDARY)])
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
