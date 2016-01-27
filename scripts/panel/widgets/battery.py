#!/usr/bin/python

import os
import sys
import re
import time
import math
from panelParams import SLEEP_BATTERY

RED='#C23B22'
GREEN='#77DD77'
YELLOW='#FDFD96'

fifoPath = os.environ['PANEL_BATTERY_FIFO']

promptCommand = """
tail -f $PANEL_BATTERY_FIFO &
while true ; do
  echo hello
  sleep """ + str(SLEEP_BATTERY) + """
done
"""

batteryCommand = """
upower -i $(upower -e | grep 'BAT') |\
  grep -E 'state|time\ to|percentage'
"""

def getBatteryDump():
  f = os.popen(batteryCommand)
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

def main():
  try:
    os.mkfifo(fifoPath)
  except:
    pass

  promptProcess = os.popen(promptCommand)
  while(1):
    print(getBatteryFormatted())
    sys.stdout.flush()
    promptProcess.readline()

if __name__ == "__main__":
  main()

