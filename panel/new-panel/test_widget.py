#!/usr/bin/python

from widget import Widget

class TestWidget(Widget):
  def __init__(self):
    self.click_command = "echo Hello"

  def get_text(self):
    return "Hello, world!"

