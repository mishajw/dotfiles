#!/usr/bin/python

import os
import sys
import re
import time
import math

RED='#C23B22'
GREEN='#77DD77'
YELLOW='#FDFD96'

def getBatteryDump():
  f = os.popen("upower -i $(upower -e | grep 'BAT') | grep -E 'state|time\ to|percentage'")
  return [re.compile("\s+").split(line) for line in f.read().split('\n')]

def getBatteryFormatted():
  battery = getBatteryDump()
  
  state = battery[0][-1]
  time = battery[1][-2] + battery[1][-1][0]
  perc = int(battery[2][-1][:-1])
  color = ''

  if state == 'charging':
    color = GREEN
    state = ' \uf0e7'
  else:
    state = ''
    if perc > 60:
      color = GREEN
    elif perc > 30:
      color = YELLOW
    else:
      color = RED

  icon = ''

  if perc > 75:
    icon = '\uf240'
  elif perc > 50:
    icon = '\uf241'
  elif perc > 25:
    icon = '\uf242'
  else:
    icon = '\uf243'

  return "%%{F%s}%s%s%%{F-} %d%% (%s)" % (color, icon, state, perc, time)
  # return "%d%% %s(%s)" % (perc, state, time)

def main():
  while(1):
    print(getBatteryFormatted())
    sys.stdout.flush()
    time.sleep(1)

if __name__ == "__main__":
  main()

