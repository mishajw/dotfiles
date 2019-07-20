#!/usr/bin/env bash

# pylint: disable=missing-docstring

import argparse
import logging
import os
from subprocess import check_call, check_output
from pathlib import Path

LOG = logging.getLogger(__name__)

INIT = Path(os.environ["init"])
USER = "misha"
DOCKER_NAME = "mk_image"

INSTALL_CMD = ["pacman", "--needed", "--noconfirm", "-S"]
BASH_CMD = ["bash", "-c"]
OS_CMD = ["docker", "exec", DOCKER_NAME]
IMG_ROOT_CMD = [*OS_CMD, "arch-chroot", "/mnt"]
IMG_USER_CMD = [*IMG_ROOT_CMD, "su", USER, "--command"]


def main():
    parser = argparse.ArgumentParser(DOCKER_NAME)
    parser.add_argument("--image", type=str, required=True)
    parser.add_argument("--boot", type=str, default=None)
    parser.add_argument("--device", type=str, default=None)
    args = parser.parse_args()
    assert (args.boot is None) == (args.device is None)

    LOG.info("Starting docker container")
    if DOCKER_NAME not in check_output(["docker", "ps"]).decode():
        LOG.info("Starting docker container")
        check_call(
            [
                "docker",
                "run",
                # In background
                "--detach",
                # frebib magic
                "--cap-add=SYS_ADMIN",
                f"--name={DOCKER_NAME}",
                # Bind mountable devices
                *[
                    f"--device={device}"
                    for device in [args.image, args.boot]
                    if device is not None
                ],
                "archlinux/base",
                # Run command that never exits
                "tail",
                "-f",
                "/dev/null",
            ]
        )

    LOG.info("Stage 1: Installing arch")
    if args.image not in check_output([*OS_CMD, "mount"]).decode():
        LOG.info("Stage 1.1: Mounting main partition")
        check_call([*OS_CMD, "mkfs.ext4", args.image])
        check_call([*OS_CMD, "mount", args.image, "/mnt"])
    check_call([*OS_CMD, "pacman", "-Sy"])
    check_call([*OS_CMD, *INSTALL_CMD, "arch-install-scripts", "dosfstools"])
    if args.boot is not None:
        LOG.info("Stage 1.2: Mounting boot partition")
        check_call([*OS_CMD, "mkfs.vfat", "-F32", args.boot])
        check_call([*OS_CMD, "mkdir", "--parents", "/mnt/boot"])
        check_call([*OS_CMD, "mount", args.boot, "/mnt/boot"])
    LOG.info("Stage 1.3: Running pacstrap")
    check_call([*OS_CMD, "pacstrap", "/mnt", "base", "base-devel"])
    check_call([*OS_CMD, *BASH_CMD, "genfstab -U /mnt >> /mnt/etc/fstab"])

    LOG.info("Stage 2: Setting up user")
    check_call(
        [*IMG_ROOT_CMD, *BASH_CMD, (INIT / "user.sh").read_text(), "--", USER]
    )

    LOG.info("Stage 3: Setting up dotfiles")
    check_call([*IMG_USER_CMD, *BASH_CMD, (INIT / "dotfiles.sh").read_text()])

    LOG.info("Stage 4: Setting up boot")
    if args.boot is not None:
        # TODO: Maybe migrate back to refind?
        # check_call([*IMG_ROOT_CMD, *INSTALL_CMD, "refind-efi"])
        # check_call([*IMG_ROOT_CMD, "refind-install"])
        check_call([*IMG_ROOT_CMD, *INSTALL_CMD, "grub"])
        check_call(
            [
                *IMG_ROOT_CMD,
                "grub-install",
                "--recheck",
                "--target=i386-pc",
                args.device,
            ]
        )
        check_call(
            [*IMG_ROOT_CMD, "grub-mkconfig", "-o", "/boot/grub/grub.cfg"]
        )

    LOG.info("Stage 5: Setting up config")
    check_call([*IMG_ROOT_CMD, *BASH_CMD, (INIT / "config.sh").read_text()])

    LOG.info("Unmounting image in docker container")
    if args.boot is not None:
        check_call([*OS_CMD, "umount", "/mnt/boot"])
    check_call([*OS_CMD, "umount", "/mnt"])


if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    main()
