#!/usr/bin/python

from datetime import datetime

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
