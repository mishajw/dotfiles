#!/usr/bin/python

import os
import time
import sys

TIME_WAIT = 60

def getIntFromOS(cmd):
  f = os.popen(cmd)
  return int(f.read())

def getUpdates():
  return getIntFromOS("pacman -Qu | wc -l")

def getExpInstalled():
  return getIntFromOS("pacman -Qe | wc -l")

def getInstalled():
  return getIntFromOS("pacman -Q | wc -l")

def main():
  while(1):
    print("\uf0aa T:%d E:%d U:%d" % (
      getInstalled(),
      getExpInstalled(),
      getUpdates()
    ))
    sys.stdout.flush()
    time.sleep(TIME_WAIT)

if __name__ == "__main__":
  main()

