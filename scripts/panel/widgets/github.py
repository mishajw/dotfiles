#!/usr/bin/python

import json
import datetime
import sys
import time
from urllib.request import urlopen

command = 'google-chrome-stable "http://github.com/mishajw"'

def main():
  while 1:
    try:
      printCommits()
    except:
      pass
    time.sleep(1)

def printCommits():
  raw = getRawJSON()
  parsed = json.loads(raw)

  times = [(event['created_at'].split("T")[0], int(event['payload']['size'])) for event in parsed]
  
  today = 0

  for (t, i) in times:
    if checkTime(t):
      today += i

  print("%%{A:%s:}\uf09b %d%%{A}" % (command, today))
  sys.stdout.flush()

def getRawJSON():
  response = urlopen('https://api.github.com/users/mishajw/events')
  return response.read().decode()

def checkTime(timeStr):
  spl = timeStr.split('-')
  year = int(spl[0])
  month = int(spl[1])
  day = int(spl[2])

  now = datetime.datetime.now()

  isToday = \
    now.year == year and \
    now.month == month and \
    now.day == day

  return isToday


if __name__ == '__main__':
  main()

