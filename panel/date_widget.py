#!/usr/bin/python

from widget import Widget
import os
import re

class DateWidget(Widget):
  
  def __init__(self):
    super(DateWidget, self).__init__()
    self.has_underline = True

  def update_text(self):
    f = os.popen("date +'%a %e %l:%M:%S %p'")
    self.text = re.sub(r" +", " ", f.read())

