#!/usr/bin/env python

import sys
import webbrowser

url = "https://explainshell.com/explain?cmd=" + "+".join(sys.argv[1:])
print("Opening " + url)
webbrowser.open(url)

