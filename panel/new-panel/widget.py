#!/usr/bin/python

from threading import Thread
import time
from panel_help import *

class Widget:
  def __init__(self):
    self.update_time = 1
    self.click_command = ""
    self.text = ""

  def update_text(self):
    return "Not implmented"

  def get_text_with_commands(self):
    if self.click_command != "":
      return set_left_click(self.text, self.click_command)
    else:
      return self.text

  def update_loop(self):
    while 1:
      time.sleep(self.update_time)
      self.update_text_with_commands()

  def start_thread(self):
    t = Thread(target=self.update_loop)
    t.start()

