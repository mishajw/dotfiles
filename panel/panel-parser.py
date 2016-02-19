#!/usr/bin/python

import sys
import time
import random

SEPARATOR = " " * 3
COLORS = ['#a0b89f', '#e1d5a9', '#e4a972']

leftProcesses = []
rightProcesses = []

def main():
  global leftProcesses
  global rightProcesses

  for input in sys.stdin:
    align = input[0]
    index = int(input[1])
    content = input[2:].replace('\n', '')

    if align == 'l':
      leftProcesses = makeRoom(leftProcesses, index)
      leftProcesses[index] = content
    elif align =='r':
      rightProcesses = makeRoom(rightProcesses, index)
      rightProcesses[index] = content

    printAll()

def printArray(a):
  output = ''

  for i in range(len(a)):
    curColor = "%%{F%s}" % COLORS[i % len(COLORS)]
    a[i] = a[i].replace('%{F-}', curColor)
    output += "%s%s%%{F-}" % (curColor, a[i])

    if i != len(a):
      output += SEPARATOR

  return output

def printAll():
  print("%%{1}%%{S1}%%{l}%s%%{r}%s" % (printArray(leftProcesses), printArray(rightProcesses)))
  sys.stdout.flush()

def makeRoom(a, i):
  while len(a) - 1 < i:
    a.append('')

  return a

if __name__ == "__main__":
  main()

