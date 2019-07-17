#!/usr/bin/env bash

# pylint: disable=missing-docstring

import argparse
import logging
import os
from subprocess import check_call, check_output
from pathlib import Path

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

DOCKER_NAME = "mk_image"
OS_CMD = ["docker", "exec", DOCKER_NAME]
IMG_ROOT_CMD = [*OS_CMD, "arch-chroot", "/mnt"]
IMG_USER_CMD = [*IMG_ROOT_CMD, "su", USER, "--command"]


def main():
    parser = argparse.ArgumentParser(DOCKER_NAME)
    parser.add_argument("--image", type=str, required=True)
    args = parser.parse_args()

    assert SRC_DIRECTORY.is_dir(), "src directory does not exist"
    if not OUTPUT_DIRECTORY.exists():
        LOG.debug("Creating output directory")
        OUTPUT_DIRECTORY.mkdir(parents=True)

    LOG.info("Starting docker container")
    if DOCKER_NAME not in check_output(["docker", "ps"]):
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
                f"--volume={SRC_DIRECTORY}:{OS_SRC_DIRECTORY}:ro",
                "archlinux/base",
                # Run command that never exits
                "tail",
                "-f",
                "/dev/null",
            ]
        )

    LOG.info("Mounting image")
    check_call([*OS_CMD, "mount", args.image, "/mnt"])
    LOG.info("Syncing packages")
    check_call([*OS_CMD, "pacman", "-Sy"])

    LOG.info("Stage 1: Installing arch")
    check_call([*OS_CMD, OS_SRC_DIRECTORY / "01-arch.sh"])
    LOG.info("Stage 1.1: Linking src to image")
    check_call([*OS_CMD, "mkdir", "--parents", "/mnt/host"])
    check_call([*OS_CMD, "mount", "--rbind", "/host", "/mnt/host"])

    LOG.info("Stage 2: Setting up user")
    check_call([*IMG_ROOT_CMD, OS_SRC_DIRECTORY / "02-user.sh"])

    LOG.info("Stage 3: Setting up dotfiles")
    check_call([*IMG_USER_CMD, OS_SRC_DIRECTORY / "03-dotfiles.sh"])

    LOG.info("Stage 4: Setting up config")
    check_call([*IMG_ROOT_CMD, OS_SRC_DIRECTORY / "04-config.sh"])

    check_call([*OS_CMD, "umount", "/mnt"])


if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    main()
