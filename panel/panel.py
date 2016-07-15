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
import re
import subprocess

colors = ['#f9d3a5', '#dbad72', '#ab9c73']
backgroundColor = '#291f0a00'
foregroundColor = '#774f38'

separator = "  "

left_items = [
  WorkspaceWidget(),
]

middle_items = [
  TitleWidget()
]

right_items = [
  VolumeWidget(),
  # BatteryWidget(),
  # GithubWidget(),
  # UpdatesWidget(),
  DateWidget()
]

lemonbar_command = \
        'lemonbar -a 100 -u 2 -g x%s -f %s -f FontAwesome -F %s -B %s' % \
        (os.environ['PANEL_HEIGHT'], "Monospace:style=bold:size=10", foregroundColor, backgroundColor)

def main():
  global stdout

  p = subprocess.Popen(lemonbar_command.split(" "), stdout=subprocess.PIPE, stdin=subprocess.PIPE)
  bash = subprocess.Popen("sh", stdout=subprocess.PIPE, stdin=p.stdout)
  setup_fifo()
  stdout = p.stdin

  start_widgets()

  print_loop()

def print_loop():
  print_full_text()

  f = open(FIFO_PATH, 'r')

  while True:
    line = f.readline()
    line = re.sub("\n", "", line)
  
    # print("^" + line + "$")

    should_update = line == "updated"

    for w in all_widgets():
      if w.__class__.__name__ == line:
        w.update_text()
        should_update = True

    if line == "":
      f = open(FIFO_PATH, 'r')

    if should_update:
      print_full_text()

def setup_fifo():
  try:
    os.mkfifo(FIFO_PATH)
  except FileExistsError:
    pass

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

  full_text = "  %%{Sf}%%{l}%s%%{c}%s%%{r}%s  " % (left_text, middle_text, right_text)

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

