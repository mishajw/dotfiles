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
  color = '#FF0000'
  
  if state == "charging":
    state = ' \uf0e7'
  else:
    state = ''

  icon = ''
  if perc > 66:
    icon = '\uf004\uf004\uf004'
  elif perc > 33:
    icon = '\uf08a\uf004\uf004'
  elif perc > 10:
    icon = '\uf08a\uf08a\uf004'
  else:
    icon = '\uf08a\uf08a\uf08a'


  return "%d%% %%{F%s}%s%s%%{F-} (%s)" % (perc, color, icon, state, time)

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

