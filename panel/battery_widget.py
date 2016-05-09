#!/usr/bin/python

from number_widget import NumberWidget
from panel_help import *
import os
import re

class BatteryWidget(NumberWidget):

  def __init__(self):
    super(BatteryWidget, self).__init__('B')
    
    self.update_time = 60

    self.battery_command = "upower -i $(upower -e | grep 'BAT') |\
      grep -E 'state|time\ to|percentage'"

  def update_number(self):
    battery = self.get_battery_dump()
    
    self.state = battery[0][-1]

    self.number = int(battery[-1][-1][:-1])

  def update_char(self):
    if self.state == 'charging':
      self.character = '%{F#00FF00}B'
    elif self.number < 20:
      self.character = '%{F#FF0000}B'
    else:
      self.character = 'B'

  def get_battery_dump(self):
    f = os.popen(self.battery_command)
    return [re.compile("\s+").split(line) for line in f.read().split('\n') if line.strip() != '']
