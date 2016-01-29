#!/usr/bin/python

import os
import stat
import re
import sys

fifoPath = os.environ['VOL_CHANGED_FIFO']
command = "amixer sset 'Master' 0% ; amixer sset 'Master' mute ; ~/scripts/vol-changed.sh"

def main():
  makeFifo()

  getVolumeDetails()

  while 1:
    f = open(fifoPath, 'r')

    for line in f:
      getVolumeDetails()

    f.close()

def getVolumeDetails():
  p = os.popen("amixer sget Master | grep 'Front Left: Playback'")
  stats = p.read()
  vol = 0
  mute = False
  icon = ''

  spl = re.split(" +", stats)

  vol = int(spl[5][1:-2])
  mute = spl[6][1:-2] == 'off'

  if vol == 0 or mute:
    icon = '\uf026'
  elif vol > 50:
    icon = '\uf028'
  else:
    icon = '\uf027'

  print("%%{A:%s:}%s %d%%%%{A}" % (command, icon, vol))
  sys.stdout.flush()

def makeFifo():
  try:
    os.mkfifo(fifoPath)
  except:
    pass

if __name__ == "__main__":
  main()

