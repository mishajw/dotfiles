#!/usr/bin/python

from panel_help import *
from widget import Widget

class NumberWidget(Widget):
  def __init__(self, init_char):
    super(NumberWidget, self).__init__()
    self.number = 0
    self.character = init_char
    self.has_underline = True

  def update_text(self):
    self.update_number()
    self.update_char()

    self.text = "%s:%d" % (self.character, self.number)

  def update_number(self):
    pass

  def update_char(self):
    pass

