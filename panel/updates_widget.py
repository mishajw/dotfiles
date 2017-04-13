#!/usr/bin/python

from number_widget import NumberWidget
import os

class UpdatesWidget(NumberWidget):
  
  def __init__(self):
    super(UpdatesWidget, self).__init__('U')
    self.click_command = "urxvt -hold -e bash -c 'sudo pacman -Syyu && echo Done updating.'"
    self.update_time = 60 * 5 
    
  def update_number(self):
    p = os.popen("yaourt -Sy; yaourt -Qyyua | wc -l")
    self.number = int(p.read())

