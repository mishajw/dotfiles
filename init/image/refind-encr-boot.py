#!/usr/bin/env python

import argparse
import re
from pathlib import Path
from subprocess import check_output

UUID_REGEX = re.compile(r"UUID=\"([a-f0-9-]+)\"")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--encrypted-device", type=str, required=True)
    parser.add_argument("--mapped-device", type=str, required=True)
    parser.add_argument("--output", type=str, default="/boot/refind_linux.conf")
    args = parser.parse_args()

    encrypted_uuid_output = check_output(["blkid", args.encrypted_device]).decode()
    match = UUID_REGEX.search(encrypted_uuid_output)
    assert match is not None
    encrypted_uuid = match.group(1)

    boot_message = f"Boot encrypted {args.mapped_device}"
    boot_options = (
        f"cryptdevice=UUID={encrypted_uuid}:cryptlvm root={args.mapped_device}"
    )
    boot_line = f'"{boot_message}"\t"{boot_options}"'

    output_path = Path(args.output)
    contents = [
        line.strip()
        for line in output_path.read_text().split("\n")]
    if boot_line in contents:
        contents.remove(boot_line)
    contents = [boot_line] + contents

    output_path.write_text("\n".join(contents))


if __name__ == "__main__":
    main()
