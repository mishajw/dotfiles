#!/usr/bin/python

from widget import Widget
from panel_help import *

class TestWidget(Widget):
  def __init__(self):
    self.click_command = "echo Hello"
    super(TestWidget, self).__init__()

  def update_text(self):
    return str(curr_time())

