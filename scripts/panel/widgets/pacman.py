#!/usr/bin/python

import os
import time
import sys
from panelParams import SLEEP_PACMAN

command = 'urxvt -hold -e sudo pacman -Syyu ; echo Done'

def getIntFromOS(cmd):
  f = os.popen(cmd)
  return int(f.read())

def getUpdates():
  return getIntFromOS("checkupdates | wc -l")

def getExpInstalled():
  return getIntFromOS("pacman -Qe | wc -l")

def getInstalled():
  return getIntFromOS("pacman -Q | wc -l")

def main():
  print('Loading...')
  sys.stdout.flush()
  while(1):
    print("%%{A:%s:}\uf0aa T:%d E:%d U:%d%%{A}" % (
      command,
      getInstalled(),
      getExpInstalled(),
      getUpdates()
    ))
    sys.stdout.flush()
    time.sleep(SLEEP_PACMAN)

if __name__ == "__main__":
  main()

