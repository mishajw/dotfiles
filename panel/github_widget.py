#!/usr/bin/python

import json
import datetime
import sys
import time
import os
import traceback
from urllib.request import urlopen
from urllib.error import URLError
from number_widget import NumberWidget

class GithubWidget(NumberWidget):
  
  def __init__(self):
    super(GithubWidget, self).__init__('G')
    self.setURL()
    self.update_time = 10

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
    
    today = 0

    for event in parsed:
      time = event['created_at'].split("T")[0]

      try:
        amount = int(event['payload']['size'])
      except:
        amount = 0

      if self.checkTime(time):
        today += amount
        
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
  
