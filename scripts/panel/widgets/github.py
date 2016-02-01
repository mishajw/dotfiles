#!/usr/bin/python

import json
import datetime
import sys
import time
from urllib.request import urlopen
from urllib.error import URLError
from panelParams import SLEEP_GITHUB

command = 'google-chrome-stable http://github.com/mishajw'

def main():
  while 1:
    try:
      printCommits()
    except URLError as e:
      printMessage('\uf119')

    time.sleep(SLEEP_GITHUB)

def printCommits():
  raw = getRawJSON()
  parsed = json.loads(raw)

  times = [(event['created_at'].split("T")[0], int(event['payload']['size'])) for event in parsed]
  
  today = 0

  for (t, i) in times:
    if checkTime(t):
      today += i
  
  printMessage(str(today))

def getRawJSON():
  response = urlopen('https://api.github.com/users/mishajw/events?access_token=43324f412e680003cee4d7395fb23e9bcfdec0a5')
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

def printMessage(amount):
  print("%%{A:%s:}\uf09b %s%%{A}" % (command, amount))
  sys.stdout.flush()

if __name__ == '__main__':
  main()

