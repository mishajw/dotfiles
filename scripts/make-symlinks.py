#!/usr/bin/env python

import json
import os

def is_absolute(path: str) -> bool:
    return len(path) > 0 and (path[0] == "~" or path[0] == "/")

default_src_dir = os.environ["cnf"] if "cnf" in os.environ else \
    os.path.join(os.environ["HOME"], "dotfiles", "config")
default_dst_dir = os.environ["HOME"]

with open(os.path.join(default_src_dir, "symlinks.json")) as f:
    json = json.load(f)

success = True

for link in json:
    link_src = link["src"]
    if "dst" in link:
        link_dst = link["dst"]
    else:
        assert not is_absolute("link_src"), \
            "If src is absolute, dst must be given"
        link_dst = os.path.join(default_dst_dir, link_src)

    if not is_absolute(link_src):
        link_src = os.path.join(default_src_dir, link_src)
    if not is_absolute(link_dst):
        link_dst = os.path.join(default_dst_dir, link_dst)

    print(f"> Making symlink: {link_src} -> {link_dst}")

    # Perform checks on whether the symlink exists already
    if os.path.isfile(link_dst):
        if os.path.islink(link_dst):
            current_link = os.readlink(link_dst)
            if current_link == link_src:
                print("Correct symlink already exists")
            else:
                print(f"ERROR: symlink exists, but points to {current_link} "
                      f"(expected {link_src})")
                success = False
        else:
            print("ERROR: normal file exists at symlink dst")
            success = False
        continue

    # Create the destination directory if it doesn't exist
    link_dst_directory, _ = os.path.split(link_dst)
    if not os.path.isdir(link_dst_directory):
        os.makedirs(link_dst_directory)
    # Make the symlink
    os.symlink(link_src, link_dst)
    print("Made symlink")

if success:
    print("Symlink creation success!")
else:
    print("Errors occured, check logs")
