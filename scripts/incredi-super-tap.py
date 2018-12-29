#!/usr/bin/env python

import subprocess
import io
import os

KEYBOARD_ID = 10
SUPER_KEY_ID = 133
INCREDIC = os.path.join(os.environ["HOME"], ".cargo/bin/incredic")

def super_tapped():
    subprocess.run([INCREDIC, "--command", "show"])

xinput_process = subprocess.Popen(
    ["xinput", "test", str(KEYBOARD_ID)], stdout=subprocess.PIPE)
last_pressed = None
for line in io.TextIOWrapper(xinput_process.stdout, encoding="utf-8"):
    _, mode, key_id = line.strip().split()
    key_id = int(key_id)

    if mode == "press":
        last_pressed = key_id
    elif mode == "release" and last_pressed == key_id and key_id == 133:
        super_tapped()

