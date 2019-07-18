#!/usr/bin/env bash

# pylint: disable=missing-docstring

import argparse
import logging
import os
from subprocess import check_call, check_output
from pathlib import Path

LOG = logging.getLogger(__name__)

DF = Path(os.environ["df"])
USER = "misha"
OUTPUT_IMAGE_SIZE_GB = 3

DOCKER_NAME = "mk_image"
INSTALL_CMD = ["pacman", "--needed", "--noconfirm", "-S"]
BASH_CMD = ["bash", "-c"]
OS_CMD = ["docker", "exec", DOCKER_NAME]
IMG_ROOT_CMD = [*OS_CMD, "arch-chroot", "/mnt"]
IMG_USER_CMD = [*IMG_ROOT_CMD, "su", USER, "--command"]


def main():
    parser = argparse.ArgumentParser(DOCKER_NAME)
    parser.add_argument("--image", type=str, required=True)
    parser.add_argument("--swap", type=str, default=None)
    parser.add_argument("--boot", type=str, default=None)
    args = parser.parse_args()

    LOG.info("Starting docker container")
    if DOCKER_NAME not in check_output(["docker", "ps"]).decode():
        check_call(
            [
                "docker",
                "run",
                # In background
                "--detach",
                # frebib magic
                "--cap-add=SYS_ADMIN",
                f"--name={DOCKER_NAME}",
                # Bind image to /dev/image
                f"--device={args.image}",
                "archlinux/base",
                # Run command that never exits
                "tail",
                "-f",
                "/dev/null",
            ]
        )

    LOG.info("Stage 0: Mounting image")
    if args.image not in check_output([*OS_CMD, "mount"]).decode():
        check_call([*OS_CMD, "mkfs.ext4", args.image])
        check_call([*OS_CMD, "mount", args.image, "/mnt"])
        if args.boot is not None:
            check_call([*OS_CMD, "mount", args.boot, "/mnt/boot"])
        if args.swap is not None:
            check_call([*OS_CMD, "swapon", args.swap])
    LOG.info("Syncing packages")
    check_call([*OS_CMD, "pacman", "-Sy"])

    LOG.info("Stage 1: Installing arch")
    check_call([*OS_CMD, *INSTALL_CMD, "arch-install-scripts"])
    check_call([*OS_CMD, "pacstrap", "/mnt", "base", "base-devel"])
    check_call([*OS_CMD, *BASH_CMD, "genfstab -U /mnt >> /mnt/etc/fstab"])

    LOG.info("Stage 2: Setting up user")
    check_call(
        [*IMG_ROOT_CMD, *BASH_CMD, (DF / "init" / "user.sh").read_text()]
    )

    LOG.info("Stage 3: Setting up dotfiles")
    check_call(
        [*IMG_USER_CMD, *BASH_CMD, (DF / "init" / "dotfiles.sh").read_text()]
    )

    LOG.info("Stage 4: Setting up config")
    check_call(
        [*IMG_ROOT_CMD, *BASH_CMD, (DF / "init" / "config.sh").read_text()]
    )

    check_call([*OS_CMD, "umount", "/mnt"])


if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    main()
