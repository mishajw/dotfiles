#!/usr/bin/python

import json
import os

srcPath = os.environ["cnf"] + "/"
dstPath = os.environ["HOME"] + "/"

def main():
  jsonRaw = getJson()
  jsonParsed = json.loads(jsonRaw)

  for link in jsonParsed["symlinks"]:
    src  = srcPath + link["src"]
    
    if "dst" in link:
      dst = dstPath + link["dst"]
    else:
      dst = dstPath + link["src"]

    try:
      os.symlink(src, dst)
      print("Made symlink %s -> %s" % (src, dst))
    except FileExistsError:
      print("Couldn't make symlink %s -> %s because file already exists" % (src, dst))
      if os.path.islink(dst) and input("File is symlink. Replace? (y/n)") == "y":
        os.remove(dst)
        os.symlink(src, dst)
        print("Replaced.")

    except Exception as e:
      print("Unexpected error: " + str(e))

def getJson():
  f = open("symlinks.json", 'r')
  text = ""
  
  for line in f:
    text += line

  return text

if __name__ == "__main__":
  main()

