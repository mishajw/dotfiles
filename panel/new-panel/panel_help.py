#!/usr/bin/python

from datetime import datetime

FIFO_PATH="/tmp/new-panel-fifo"

def set_color(s, color):
  return "%%{F%s}%s%%{F-}" % (color, s)

def set_background_color(s, color):
  return "%%{B%s}%s%%{B-}" % (color, s)

def set_all_colors(s, fg, bg):
  return set_background_color(set_color(s, fg), bg)

def set_left_click(s, command):
  return "%%{A:%s:}%s%%{A}" % (command, s)

def curr_time():
  return datetime.now().microsecond

def registerUpdate():
  print_to_fifo("updated")

def print_to_fifo(s):
  f = open(FIFO_PATH, 'w')
  f.write(s + "\n")
  f.close()

