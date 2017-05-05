#!/usr/bin/python

from datetime import datetime
import os

FIFO_PATH = os.environ["PANEL_FIFO"]


def set_color(s, color):
    return "%%{F%s}%s%%{F-}" % (color, s)


def set_background_color(s, color):
    return "%%{B%s}%s%%{B-}" % (color, s)


def set_underline_color(s, color):
    return "%%{U%s}%%{+u}%s%%{-u}%%{U-}" % (color, s)


def set_all_colors(s, fg, bg):
    return set_background_color(set_color(s, fg), bg)


def set_left_click(s, command):
    return "%%{A:%s:}%s%%{A}" % (command, s)


def curr_time():
    return datetime.now().microsecond


def register_update():
    print_to_fifo("updated")


def print_to_fifo(s):
    fifo = open(FIFO_PATH, 'w')
    fifo.write(s + "\n")
    fifo.flush()
    fifo.close()


def darken_color(c):
    c = c[1:]
    split = [c[i:i + 2] for i in range(0, len(c), 2)]
    ints = [int(h, 16) for h in split]
    lowered = [int(i * 0.8) for i in ints]
    loweredHex = [hex(i) for i in lowered]
    formatted = [str(h)[2:] for h in loweredHex]

    final = "#"

    for h in formatted:
        if len(h) == 1:
            final += "0" + h
        else:
            final += h

    return final
