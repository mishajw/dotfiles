#!/usr/bin/python

import os
import subprocess
import re

p = os.popen("nload wlp4s0")

while 1:
  for line in p:
    r = re.search('Curr: .* Bit', line)

    if r:
      print("SPEED:" + r.group(0) + "END")

