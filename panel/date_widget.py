#!/usr/bin/python

from widget import Widget
import os

class DateWidget(Widget):
  
  def __init__(self):
    super(DateWidget, self).__init__()

  def update_text(self):
    f = os.popen("date +'%a %e %l:%M:%S %p'")
    self.text = f.read()

