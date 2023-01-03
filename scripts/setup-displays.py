#!/usr/bin/env python

"""
Sets up monitors using xrandr.
"""

from subprocess import check_output, check_call
from typing import Iterator, List, Dict, Tuple, Set
import sys


DESKTOPS_SOLO = [str(i) for i in range(1, 10)] + ["dmp"]
DESKTOPS_PRIMARY = [str(i) for i in range(1, 8)] + ["dmp"]
DESKTOPS_SECONDARY = ["a", "b"]


def main():
    monitors = set(get_connected_monitors())
    print("Connected monitors: " + ", ".join(monitors))

    # if monitors == {"eDP1"}:
    #     run_xrandr(["--output eDP1 --primary --auto --scale 1x1", "--output DP1 --off"])
    #     set_desktops([("eDP1", DESKTOPS_SOLO)])
    if monitors == {"screen"}:
        run_xrandr(["--output screen --primary --auto"])
        set_desktops([("screen", DESKTOPS_SOLO)])
    # elif monitors == {"eDP1", "DP1"}:
    #     run_xrandr(
    #         [
    #             "--output DP1 --primary --auto",
    #             "--output eDP1 --same-as DP1 --scale-from 2560x1440 --size 1920x1080",
    #         ]
    #     )
    #     set_desktops([("eDP1", DESKTOPS_SOLO)])
    #     check_call(["bspc", "monitor", "DP1", "--remove"])
    elif monitors == {"eDP-1", "DP-1"}:
        run_xrandr(
            [
                "--output eDP-1 --primary --mode 3840x2160 --auto",
                "--output DP-1 --same-as eDP-1 --mode 3840x2160 --auto",
            ]
        )
        set_desktops([("eDP-1", DESKTOPS_SOLO)])
    elif monitors == {"eDP-1", "DP-2"}:
        run_xrandr(
            [
                "--output eDP-1 --primary --mode 2560x1440 --auto",
                # "--addmode HDMI-1 2560x1440",
                "--output DP-2 --same-as eDP-1 --mode 2560x1440 --auto",
            ]
        )
        set_desktops([("eDP-1", DESKTOPS_SOLO)])
    elif monitors == {"eDP-1"}:
        run_xrandr(
            [
                "--output eDP-1 --mode 2048x1152 --auto --primary",
            ]
        )
        set_desktops([("eDP-1", DESKTOPS_SOLO)])
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


def get_bspwm_monitors() -> Set[str]:
    return set(
        check_output(["bspc", "query", "--monitors", "--names"]).decode().strip().split("\n")
    )


def get_active_monitors() -> Iterator[str]:
    lines = check_output(["xrandr", "--listactivemonitors"]).decode().strip().split("\n")
    for line in lines:
        if "Monitors:" in line:
            continue
        yield line.split()[-1]


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

    selected_monitors = {monitor for monitor, desktops in monitor_desktops}
    remove_redundant_monitors(selected_monitors)


def remove_redundant_monitors(selected: Set[str]):
    connected = set(get_connected_monitors())
    active = set(get_active_monitors())
    bspwm = get_bspwm_monitors()

    for monitor in bspwm - selected:
        print("Removing redundant BSPWM monitor: ", monitor)
        check_call(["bspc", "monitor", monitor, "--remove"])
    # Selected monitors might still be on if they're mirroring other monitors.
    for monitor in active - connected:
        print("Removing redundant active monitor: ", monitor)
        check_call(["xrandr", "--output", monitor, "--off"])


if __name__ == "__main__":
    main()
