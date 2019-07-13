#!/usr/bin/env bash

# pylint: disable=missing-docstring

import logging
import os
import subprocess
from pathlib import Path
from typing import List

LOG = logging.getLogger(__name__)

MAIN_DIRECTORY = Path(os.environ["HOME"]) / "dotfiles" / "init" / "image"
SRC_DIRECTORY = MAIN_DIRECTORY / "src"
OUTPUT_DIRECTORY = MAIN_DIRECTORY / "output"
IMAGE_DIRECTORY = OUTPUT_DIRECTORY / "image.qcow2"

OS_MAIN_DIRECTORY = Path("/host")
OS_SRC_DIRECTORY = OS_MAIN_DIRECTORY / "src"
OS_OUTPUT_DIRECTORY = OS_MAIN_DIRECTORY / "output"
OS_IMAGE_DIRECTORY = OS_OUTPUT_DIRECTORY / "image.qcow2"

USER = "misha"
OUTPUT_IMAGE_SIZE_GB = 3


def main():
    assert SRC_DIRECTORY.is_dir(), "src directory does not exist"
    if not OUTPUT_DIRECTORY.exists():
        LOG.debug("Creating output directory")
        OUTPUT_DIRECTORY.mkdir(parents=True)

    check_command_installed("vagrant")
    check_command_installed("qemu-imag")

    if not IMAGE_DIRECTORY.exists():
        LOG.info("Creating output image %s", IMAGE_DIRECTORY)
        run_local(
            [
                "qemu-img",
                "create",
                "-f",
                "qcow2",
                IMAGE_DIRECTORY,
                f"{OUTPUT_IMAGE_SIZE_GB}G",
            ]
        )

    LOG.info("Starting vagrant")
    run_local(["vagrant", "up"])

    LOG.info("Stage 0: Mount image")
    run_os([OS_SRC_DIRECTORY / "00-mount.sh", OS_IMAGE_DIRECTORY])

    LOG.info("Stage 1: Installing arch")
    run_os([OS_SRC_DIRECTORY / "01-arch.sh"])
    LOG.info("Stage 1.1: Linking src to image")
    run_os(["mkdir", "--parents", "/mnt/host"])
    run_os(["mount", "--rbind", "/host", "/mnt/host"])

    LOG.info("Stage 2: Setting up user")
    run_chroot_root([OS_SRC_DIRECTORY / "02-user.sh"])

    LOG.info("Stage 3: Setting up dotfiles")
    run_chroot_user([OS_SRC_DIRECTORY / "03-dotfiles.sh"])

    LOG.info("Stage 4: Setting up config")
    run_chroot_root([OS_SRC_DIRECTORY / "04-config.sh"])

    run_os(["umount", "/mnt"])


def run_local(command: List[str]) -> None:
    LOG.debug("Running command: %s", command)
    subprocess.check_call(command, cwd=str(MAIN_DIRECTORY))


def run_os(command: List[str]) -> None:
    command = build_command(command)
    LOG.debug("Running command on installation OS: %s", command)
    run_local(["vagrant", "ssh", "--command", f"sudo {command}"])


def run_chroot_root(command: List[str]) -> None:
    command = build_command(command)
    LOG.debug("Running command on image as sudo: %s", command)
    command = f"sudo arch-chroot /mnt {command}"
    run_local(["vagrant", "ssh", "--command", command])


def run_chroot_user(command: List[str]) -> None:
    command = build_command(command)
    LOG.debug("Running command on image as sudo: %s", command)
    command = f"sudo arch-chroot /mnt su {USER} --command {command}"
    run_local(["vagrant", "ssh", "--command", command])


def check_command_installed(command_name: str) -> None:
    try:
        run_local(["which", command_name])
    except subprocess.CalledProcessError as err:
        raise AssertionError(f"Command {command_name} does not exist", err)


def build_command(command: List[str]) -> str:
    command = list(map(str, command))
    assert not any(
        " " in c for c in command
    ), "Spaces in OS command arguments can break"
    return " ".join(command)


if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    main()
