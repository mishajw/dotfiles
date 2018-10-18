#!/usr/bin/env python3.6

from evpn_widget import EvpnWidget
from volume_widget import VolumeWidget
from workspace_widget import WorkspaceWidget
from title_widget import TitleWidget
from battery_widget import BatteryWidget
from date_widget import DateWidget
from github_widget import GithubWidget
from updates_widget import UpdatesWidget

from panel_help import *

import os
import re
import subprocess
import logging

LOG = logging.getLogger(__name__)

colors = ['#f9d3a5', '#dbad72', '#ab9c73']
backgroundColor = '#ee291f0a'
foregroundColor = '#774f38'

separator = "  "

left_items = [
    WorkspaceWidget(),
]

middle_items = [
    TitleWidget()
]

right_items = [
    VolumeWidget(),
    BatteryWidget(),
    GithubWidget(),
    UpdatesWidget(),
    DateWidget()
]

lemonbar_command = \
    'lemonbar -a 100 -u 2 -g x%s -F %s -B %s' % \
    (os.environ['PANEL_HEIGHT'], foregroundColor, backgroundColor)


def main():
    LOG.info("Starting")
    lemonbar_process = subprocess.Popen(
        lemonbar_command.split(" "),
        stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    subprocess.Popen("sh", stdout=subprocess.PIPE, stdin=lemonbar_process.stdout)
    setup_fifo()
    stdout = lemonbar_process.stdin

    start_widgets()

    print_loop(stdout)


def print_loop(stdout):
    print_full_text(stdout)

    f = open(FIFO_PATH, 'r')

    while True:
        line = f.readline().strip()
        should_update = line == "updated"

        for w in all_widgets():
            if w.__class__.__name__ == line:
                w.update_text()
                should_update = True

        if should_update:
            print_full_text(stdout)


def setup_fifo():
    try:
        os.mkfifo(FIFO_PATH)
    except FileExistsError:
        pass


def print_full_text(stdout):
    full_text = get_full_text()
    stdout.write(full_text.encode())
    stdout.flush()


def start_widgets():
    for w in all_widgets():
        w.start_thread()


def get_full_text():
    left_text = get_items_text(left_items)
    middle_text = get_items_text(middle_items)
    right_text = get_items_text(right_items)

    full_text = "%%{Sl}%%{l}%s%%{c}%s%%{r}%s\n" % (left_text, middle_text, right_text)

    return full_text


def get_items_text(items):
    all_text = [i.get_text_with_commands() for i in items]

    colored_text = []

    for i in range(len(all_text)):
        color = colors[i % len(colors)]
        colored = set_color(all_text[i], color)

        if items[i].has_underline:
            colored = set_underline_color(colored, color)

        colored_text.append(colored)

    full_text = separator.join(colored_text)

    return full_text


def all_widgets():
    return left_items + middle_items + right_items


if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    main()
