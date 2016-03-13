#!/usr/bin/python

from number_widget import NumberWidget
import os

class UpdatesWidget(NumberWidget):
  
  def __init__(self):
    super(UpdatesWidget, self).__init__('U')
    
  def update_number(self):
    p = os.popen("checkupdates | wc -l")
    self.number = int(p.read())

