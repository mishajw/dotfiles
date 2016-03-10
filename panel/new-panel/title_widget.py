#!/usr/bin/python

from command_widget import CommandWidget
from panel_help import *

class TitleWidget(CommandWidget):
  
  def __init__(self):
    super(TitleWidget, self).__init__("xtitle -sf '%s' -t 40")

  def handle_output(self, output):
    self.text = output.decode()
    registerUpdate()

