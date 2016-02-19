#!/usr/bin/python

import os
import sys
import time
import re
from panelParams import SLEEP_CPU

command = 'urxvt -e htop'

def main():
  while(1):
    p = os.popen("mpstat")
    stats = p.read()
    idle = stats[-7:]
    try:
      used = 100 - float([re.split(' +', line)[-1] for line in stats.split('\n') if "all" in line][0])
      print("%%{A:%s:}\uf017 %.2f%%%%{A}" % (command, used))
      sys.stdout.flush()
    except:
      pass

    time.sleep(SLEEP_CPU)

  process.close()

if __name__ == "__main__":
  main()

