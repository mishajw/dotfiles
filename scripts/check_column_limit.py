#!/usr/bin/env python

import mimetypes
import os
import sys


root_directory = sys.argv[1]
max_columns = int(sys.argv[2])


def main():
    for current_directory, sub_directories, files in os.walk(root_directory):
        for file in files:
            type, _ = mimetypes.guess_type(file)
            if type is not None and "text" in type:
                process(os.path.join(current_directory, file))


def process(file_name):
    failed_lines = []

    with open(file_name, "r") as file:
        for i, line in enumerate(file):
            line = line.replace("\t", "    ")
            line = line.rstrip()
            if len(line) > max_columns:
                failed_lines.append((i, line))

    if failed_lines:
        print("File %s had %d failed lines" % (file_name, len(failed_lines)))
        
        for line_number, line in failed_lines:
            print("%d (%d lines): %s" % (line_number + 1, len(line), line[:max_columns]))


if __name__ == "__main__":
    main()

