#!/usr/bin/python

import subprocess
import sys

def main():
  process = subprocess.Popen(
    'mpstat 5'.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE
  )

  while(1):
    stats = process.stdout.readline().decode()
    idle = stats[-7:]

    try:
      used = 100 - float(idle)
      print("\uf017 %.2f%%" % used)
      sys.stdout.flush()
    except:
      pass

    sys.stdout.flush()

  process.close()

if __name__ == "__main__":
  main()

