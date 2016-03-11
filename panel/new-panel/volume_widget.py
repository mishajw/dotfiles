#!/usr/bin/python

from panel_help import *
from number_widget import NumberWidget
import os
import re

class VolumeWidget(NumberWidget):
  def __init__(self):
    super(VolumeWidget, self).__init__('V')
    self.mute = False

  def update_number(self):
    p = os.popen("amixer sget Master | grep 'Front Left: Playback'")
    stats = p.read()

    spl = re.split(" +", stats)

    self.number = int(spl[5][1:-2])
    self.mute = spl[6][1:-2] == 'off'

  def update_char(self):
    if self.number == 0 or self.mute:
      self.character = '\uf026'
    elif vol > 50:
      self.character = '\uf028'
    else:
      self.character = '\uf027'
