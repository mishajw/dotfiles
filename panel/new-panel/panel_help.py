#!/usr/bin/python

def set_color(s, color):
  return "%%{F%s}%s%%{F-}" % (color, s)

def set_left_click(s, command):
  return "%%{A:%s:}%s%%{A}" % (command, s)
