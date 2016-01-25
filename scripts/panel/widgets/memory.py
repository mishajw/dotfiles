#!/usr/bin/python

import subprocess
import sys
import time
import re

UPDATE_TIME = 1

def main():

  while(1):
    process = subprocess.Popen(
      'free -m'.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stats = process.stdout.read().decode()

    for line in stats.split('\n'):
      if line[:3] != "Mem":
        continue
    
      split = re.split(" +", line)

      perc = int(split[2]) / int(split[1]) * 100

      print("\uf02a %.2f%%" % perc)

      break
    

    sys.stdout.flush()

    time.sleep(UPDATE_TIME)

    process.kill()


if __name__ == "__main__":
  main()

