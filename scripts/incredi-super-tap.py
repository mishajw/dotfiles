#!/usr/bin/env python

import io
import os
import re
import subprocess

SUPER_KEY_ID = 133
INCREDIC = os.path.join(os.environ["HOME"], ".cargo/bin/incredic")

# Listens to all keypresses from all keyboards
BASH_COMMAND = """
xinput list |
    grep -Po 'id=[0-9]+' |
    grep -Po '[0-9]+' |
    xargs --max-procs 100 -I% xinput test %
"""


xinput_process = subprocess.Popen(
    ["bash", "-c", BASH_COMMAND], stdout=subprocess.PIPE
)
last_id = None
for line in io.TextIOWrapper(xinput_process.stdout, encoding="utf-8"):
    _, mode, current_id = line.strip().split()
    current_id = int(current_id)

    if mode == "press":
        last_id = current_id
    elif (
        mode == "release"
        and last_id == current_id
        and current_id == SUPER_KEY_ID
    ):
        subprocess.run([INCREDIC, "--command", "show"])
