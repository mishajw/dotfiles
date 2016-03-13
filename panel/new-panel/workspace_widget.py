#!/usr/bin/python

from command_widget import CommandWidget
from panel_help import *

COLOR_USED = '#FFFFFF'
COLOR_OPEN_EMPTY = '#999999'

class WorkspaceWidget(CommandWidget):

  def __init__(self):
    super(WorkspaceWidget, self).__init__("bspc control --subscribe")

  def handle_output(self, output):
    workspaces = str(output).split(":")
  
    allWorkspaces = []

    for w in workspaces:
      label = w[0]
      title = w[1:]

      dont_draw = False

      # Occupied, not active
      if label == "o":
        title = set_color(title, COLOR_USED)
      elif label == "F":
        title = set_color(title, COLOR_OPEN_EMPTY)
        title = set_underline_color(title, COLOR_USED)
      elif label == "O":
        title = set_color(title, COLOR_USED)
        title = set_underline_color(title, COLOR_USED)
      else:
        dont_draw = True

      if not dont_draw:
        allWorkspaces.append(" %s " % (title))
    
    self.text = "".join(allWorkspaces)
    registerUpdate()

