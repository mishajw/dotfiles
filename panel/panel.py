#!/usr/bin/python

from volume_widget import VolumeWidget
from workspace_widget import WorkspaceWidget
from title_widget import TitleWidget
from battery_widget import BatteryWidget
from date_widget import DateWidget
from github_widget import GithubWidget
from updates_widget import UpdatesWidget

from panel_help import *

import time
import sys
import os
import subprocess

colors = ['#a0b89f', '#e1d5a9', '#e4a972']
backgroundColor = '#33000000'
foregroundColor = '#ff888888'

separator = "  "

left_items = [
  WorkspaceWidget(),
  TitleWidget()
]

middle_items = []

right_items = [
  VolumeWidget(),
  BatteryWidget(),
  GithubWidget(),
  UpdatesWidget(),
  DateWidget()
]

lemonbar_command = \
        'lemonbar -g x%s -f %s -f "FontAwesome" -F %s -B %s' % \
        (os.environ['BAR_HEIGHT'], os.environ['MAIN_FONT'], foregroundColor, backgroundColor)

def main():
  global stdout
  p = subprocess.Popen(lemonbar_command.split(" "), stdout=subprocess.PIPE, stdin=subprocess.PIPE)
  
  setup_fifo()

  stdout = p.stdin
  start_widgets()

  print_loop()

def print_loop():
  f = open(FIFO_PATH, 'r')

  registerUpdate()

  print_full_text()

  while True:
    line = f.readline()[:-1] # Trim the new line character off

    if line == "updated":
      print_full_text()

def setup_fifo():
  try:
    os.mkfifo(FIFO_PATH)
    print("Made fifo at %s" % FIFO_PATH)
  except FileExistsError:
    print("Didn't make fifo, because already exists")

def print_full_text():
  full_text = get_full_text()
  
  global stdout
  stdout.write(full_text.encode())
  stdout.flush()

def start_widgets():
  for w in all_widgets():
    w.start_thread()

def get_full_text():
  left_text = get_items_text(left_items)
  middle_text = get_items_text(middle_items)
  right_text = get_items_text(right_items)

  full_text = "  %%{Sl}%%{l}%s%%{c}%s%%{r}%s  " % (left_text, middle_text, right_text)

  return full_text
    
def get_items_text(items):
  all_text = [i.get_text_with_commands() for i in items]

  colored_text = []

  for i in range(len(all_text)):
    color = colors[i % len(colors)]
    colored = set_color(all_text[i], color)

    if (items[i].has_underline):
      colored = set_underline_color(colored, color)

    colored_text.append(colored)

  full_text = separator.join(colored_text)

  return full_text

def all_widgets():
  return left_items + middle_items + right_items
    
if __name__ == "__main__":
  main()
  ww = WorkspaceWidget()
  ww.update_loop()
