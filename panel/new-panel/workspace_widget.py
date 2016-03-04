#!/usr/bin/python

from command_widget import CommandWidget
from panel_help import *

COLOR_CUR = ("#FF888888", "#FF58C5F1")
COLOR_ACTIVE = ("#FF58C5F1", "#FF888888")
COLOR_CUR_DISPLAY = ("#FF0000", "#00FF00")

class WorkspaceWidget(CommandWidget):

  def __init__(self):
    super(WorkspaceWidget, self).__init__("bspc control --subscribe")

  def handle_output(self, output):
    workspaces = str(output).split(":")
  
    allWorkspaces = []

    for w in workspaces:
      label = w[0]
      title = w[1:]

      color = ("", "")
      dont_draw = False

      # Occupied, not active
      if label == "o":
        color = COLOR_ACTIVE
      elif label == "O":
        color = COLOR_CUR
      elif label == "W":
        color = COLOR_CUR_DISPLAY
      else:
        dont_draw = True

      if not dont_draw:
        allWorkspaces.append(set_all_colors(" %s " % (title), color[0], color[1]))
    
    self.text = "".join(allWorkspaces)


