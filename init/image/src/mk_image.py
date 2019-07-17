#!/usr/bin/env bash

# pylint: disable=missing-docstring

import argparse
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
    parser = argparse.ArgumentParser("mk_image")
    parser.add_argument("--image", type=str, required=True)
    args = parser.parse_args()

    assert SRC_DIRECTORY.is_dir(), "src directory does not exist"
    if not OUTPUT_DIRECTORY.exists():
        LOG.debug("Creating output directory")
        OUTPUT_DIRECTORY.mkdir(parents=True)

    check_command_installed("docker")

    LOG.info("Starting docker container")
    # TODO: check if container is already running
    run_local(
        [
            "docker",
            "run",
            # In background
            "--detach",
            # frebib magic
            "--cap-add=SYS_ADMIN",
            "--name=mk_image",
            # Bind image to /dev/image
            f"--device={args.image}",
            f"--volume={SRC_DIRECTORY}:{OS_SRC_DIRECTORY}:ro",
            "archlinux/base",
            # Run command that never exits
            "tail",
            "-f",
            "/dev/null",
        ]
    )

    LOG.info("Mounting image")
    run_os(["mount", args.image, "/mnt"])
    LOG.info("Syncing packages")
    run_os(["pacman", "-Sy"])

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
    LOG.debug("Running command on installation OS: %s", command)
    run_local(["docker", "exec", "mk_image", *command])


def run_chroot_root(command: List[str]) -> None:
    LOG.debug("Running command on image as sudo: %s", command)
    run_local(["docker", "exec", "mk_image", "arch-chroot", "/mnt", *command])


def run_chroot_user(command: List[str]) -> None:
    LOG.debug("Running command on image as sudo: %s", command)
    run_local(["docker", "exec", "mk_image", "su", USER, "--command", *command])


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
