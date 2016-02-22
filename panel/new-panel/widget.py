#!/usr/bin/python

from panel_help import *

class Widget:
  def __init__(self):
    self.update_time = 0
    self.click_command = ""

  def get_text(self):
    return "Not implmented"

  def get_text_with_commands(self):
    text = self.get_text()

    if self.click_command != "":
      text = set_left_click(text, self.click_command)
    
    return text
