#!/usr/bin/python

import subprocess
import sys
import time
import re
import os
from panelParams import SLEEP_MEMORY

def main():

  while(1):
    p = os.popen('free -m')

    try:
      stats = [re.split(' +', line) for line in p.read().split('\n') if 'Mem' in line][0] 
      perc = int(stats[2]) / int(stats[1]) * 100

      print("\uf02a %.2f%%" % perc)
      sys.stdout.flush()
    except:
      pass

    time.sleep(SLEEP_MEMORY)

if __name__ == "__main__":
  main()

