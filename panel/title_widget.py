#!/usr/bin/python

from command_widget import CommandWidget
from panel_help import *


class TitleWidget(CommandWidget):
    def __init__(self):
        super(TitleWidget, self).__init__("xtitle -sf '%s'")

    def handle_output(self, output):
        self.text = "%{-u}" + output.decode().replace("\n", "")
        register_update()
