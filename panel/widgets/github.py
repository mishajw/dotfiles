#!/usr/bin/python

import json
import datetime
import sys
import time
import os
from urllib.request import urlopen
from urllib.error import URLError
from panelParams import SLEEP_GITHUB

url = ''
command = 'google-chrome-stable github.com/mishajw'

def main():
  setURL()

  while 1:
    try:
      printCommits()
    except:
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
  global url

  response = urlopen(url)
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

def setURL():
  global url
  tokenPath = os.environ['PANEL_PATH'] + "/widgets/git_token"
  f = open(tokenPath, 'r')
  token = f.read()

  url = 'https://api.github.com/users/mishajw/events?access_token=' + token 

if __name__ == '__main__':
  main()

