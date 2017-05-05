#!/usr/bin/python

from widget import Widget
import os

class EvpnWidget(Widget):
  def __init__(self):
    super().__init__()
    self.has_underline = True
    self.click_command = "expressvpn connect ; echo EvpnWidget > $PANEL_FIFO"

  def update_text(self):
    f = os.popen("expressvpn status")
    status_string = f.read()

    status = ""

    if status_string.startswith("Connected to"):
      status = "Y"
    elif status_string.startswith("Not connected."):
      status = "N"

    self.text = "VPN: " + status
