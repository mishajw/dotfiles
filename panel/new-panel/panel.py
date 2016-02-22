#!/usr/bin/python

from test_widget import TestWidget
from panel_help import *

colors = [
  "#FF0000",
  "#00FF00",
  "#0000FF"
]

separator = " | "

left_items = [
  TestWidget(),
  TestWidget(),
]

middle_items = []

right_items = []

def main():
  full_text = get_full_text
  print(full_text)

def get_full_text(items):
  left_text = get_items_text(left_items)
  middle_text = get_items_text(middle_items)
  right_text = get_items_text(right_items)

  full_text = "%%{l}%s%%{c}%s%%{r}%s" % (left_text, middle_text, right_text)

  return full_text
    
def get_items_text(items):
  full_text = ""

  for i in range(len(items)):
    cur_item = items[i]
    cur_color = colors[i % len(colors)]

    cur_text = cur_item.get_text_with_commands()
    cur_text = set_color(cur_text, cur_color)

    full_text += cur_text

  all_text = [i.get_text_with_commands() for i in items]
  colored_text = [set_color(all_text[i], colors[i % len(colors)]) for i in range(len(all_text))]
  full_text = separator.join(colored_text)

  return full_text
    
if __name__ == "__main__":
  main()
