#!/usr/bin/env python

import io
import os
import subprocess

SUPER_KEY_ID = 133
INCREDIC = os.path.join(os.environ["HOME"], ".cargo/bin/incredic")
KEYBOARD_NAME = os.environ["KEYBOARD_NAME"]

def super_tapped():
    subprocess.run([INCREDIC, "--command", "show"])

keyboard_id = int(subprocess.check_output(
    ["xinput", "--list", "--id-only", KEYBOARD_NAME]))
xinput_process = subprocess.Popen(
    ["xinput", "test", str(keyboard_id)], stdout=subprocess.PIPE)
last_pressed = None
for line in io.TextIOWrapper(xinput_process.stdout, encoding="utf-8"):
    _, mode, key_id = line.strip().split()
    key_id = int(key_id)

    if mode == "press":
        last_pressed = key_id
    elif mode == "release" and last_pressed == key_id and key_id == 133:
        super_tapped()

