#!/usr/bin/python

import subprocess

from command_widget import CommandWidget
from panel_help import *


class TitleWidget(CommandWidget):
    def __init__(self):
        print("title init")
        super(TitleWidget, self).__init__(
            "xprop -spy -root _NET_ACTIVE_WINDOW")

    def handle_output(self, output):
        window_id = output.decode().split(" ")[-1]

        window_name = subprocess.run(
            ["xdotool", "getwindowname", window_id],
            stdout=subprocess.PIPE).stdout.decode().strip()

        self.text = "%{-u}" + window_name
        register_update()
