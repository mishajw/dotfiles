#!/usr/bin/python

import json
import datetime
import sys
import time
import os
from urllib.request import urlopen
from urllib.error import URLError
from number_widget import NumberWidget

class GithubWidget(NumberWidget):
  
  def __init__(self):
    super(GithubWidget, self).__init__('G')
    self.setURL()

  def update_number(self):
    try:
      self.number = self.getCommits()
    except Exception as e:
      print("Couldn't get github commits")
      print(e)
      self.number = 0
  
  def getCommits(self):
    raw = self.getRawJSON()
    parsed = json.loads(raw)
  
    times = [(event['created_at'].split("T")[0], int(event['payload']['size'])) for event in parsed]
    
    today = 0
  
    for (t, i) in times:
      if self.checkTime(t):
        today += i
    
    return today
  
  def getRawJSON(self):
    global url
  
    response = urlopen(url)
    return response.read().decode()
  
  def checkTime(self, timeStr):
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
  
  def printMessage(self, amount):
    print("%%{A:%s:}\uf09b %s%%{A}" % (command, amount))
    sys.stdout.flush()
  
  def setURL(self):
    global url
    tokenPath = os.environ['PANEL_PATH'] + "/git_token"
    f = open(tokenPath, 'r')
    token = f.read()
  
    url = 'https://api.github.com/users/mishajw/events?access_token=' + token 
  
