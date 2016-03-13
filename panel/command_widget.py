#!/usr/bin/python

from widget import Widget
import subprocess

class CommandWidget(Widget):
  def __init__(self, command):
    self.command = command
    super(CommandWidget, self).__init__()

  
  def update_loop(self):
    p = subprocess.Popen([self.command], shell=True, stdout=subprocess.PIPE)
   
    while 1:
      l = p.stdout.readline()
      self.handle_output(l)

  def handle_output(self):
    pass

  def update_text(self):
    pass

