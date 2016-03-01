#!/usr/bin/python

from command_widget import CommandWidget

class WorkspaceWidget(CommandWidget):
  def __init__(self):
    super(WorkspaceWidget, self).__init__("bspc control --subscribe")
    self.click_command = "echo Hello, world!"

  def handle_output(self, output):
    self.text = output

