#!/usr/bin/env python

import argparse
import os
import zipfile

parser = argparse.ArgumentParser("backup-file-list")
parser.add_argument("--file-list", "-f", required=True, type=str)
parser.add_argument("--output", "-o", default="backup.zip", type=str)
args = parser.parse_args()

def get_file_paths():
    with open(args.file_list, "r") as f:
        for line in f:
            file_path = os.path.expanduser(line.strip())
            if not os.path.isdir(file_path):
                yield file_path
                continue
            for directory, _, file_names in os.walk(file_path):
                for file_name in file_names:
                    yield os.path.join(directory, file_name)

files = list(get_file_paths())

print("Backing up:")
for f in files:
    print(f"- {f}")

with zipfile.ZipFile(args.output, "w", zipfile.ZIP_DEFLATED) as zf:
    for f in files:
        zf.write(f)
print("Done")
