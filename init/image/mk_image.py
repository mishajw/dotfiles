#!/usr/bin/env bash

# pylint: disable=missing-docstring

import argparse
import logging
import os
from subprocess import check_call, check_output
from pathlib import Path

LOG = logging.getLogger(__name__)

USER = "misha"
DOCKER_NAME = "mk_image"


def main():
    parser = argparse.ArgumentParser(DOCKER_NAME)
    parser.add_argument("--image", type=str, required=True)
    parser.add_argument("--mount-path", type=str, required=True)
    parser.add_argument("--init-path", type=str, default=None)
    parser.add_argument("--boot", type=str, default=None)
    parser.add_argument("--device", type=str, default=None)
    parser.add_argument("--use-docker", type=bool, default=False)
    args = parser.parse_args()
    mnt = Path(args.mount_path)
    init = (
        Path(args.init_path)
        if args.init_path is not None
        else Path(os.environ["init"])
    )
    assert (args.boot is None) == (args.device is None)

    install_cmd = ["pacman", "--needed", "--noconfirm", "-S"]
    bash_cmd = ["bash", "-c"]
    os_cmd = ["docker", "exec", docker_name] if args.use_docker else []
    img_root_cmd = [*os_cmd, "arch-chroot", mnt]
    img_user_cmd = [*img_root_cmd, "su", USER, "--command"]

    LOG.info("Starting docker container")
    if (
        args.use_docker
        and DOCKER_NAME not in check_output(["docker", "ps"]).decode()
    ):
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
                    for device in [args.image, args.boot, args.device]
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
    mount_output = check_output([*os_cmd, "mount"]).decode()
    if args.image not in mount_output:
        LOG.info("Stage 1.1: Mounting main partition")
        check_call([*os_cmd, "mkfs.ext4", args.image])
        check_call([*os_cmd, "mount", args.image, args.mount_path])
    check_call([*os_cmd, "pacman", "-Sy"])
    check_call([*os_cmd, *install_cmd, "arch-install-scripts", "dosfstools"])
    if args.boot is not None:
        LOG.info("Stage 1.2: Mounting boot partition")
        check_call([*os_cmd, "mkdir", "--parents", mnt / "boot"])
        check_call([*os_cmd, "mount", args.boot, mnt / "boot"])
    LOG.info("Stage 1.3: Running pacstrap")
    check_call([*os_cmd, "pacstrap", mnt, "base", "base-devel"])
    check_call(
        [*os_cmd, *bash_cmd, f"genfstab -U {mnt} >> {mnt / 'etc' / 'fstab'}"]
    )

    LOG.info("Stage 2: Setting up boot")
    if args.boot is not None:
        check_call([*img_root_cmd, *install_cmd, "refind-efi"])
        check_call([*img_root_cmd, "refind-install"])

    LOG.info("Stage 3: Setting up config")
    check_call([*img_root_cmd, *bash_cmd, (init / "config.sh").read_text()])

    LOG.info("Stage 4: Setting up user")
    check_call(
        [*img_root_cmd, *bash_cmd, (init / "user.sh").read_text(), "--", USER]
    )

    LOG.info("Stage 5: Setting up dotfiles")
    check_call([*img_root_cmd, *install_cmd, "git", "zsh", "python"])
    check_call([*img_user_cmd, *bash_cmd, (init / "dotfiles.sh").read_text()])

    LOG.info("Unmounting image in docker container")
    if args.boot is not None:
        check_call([*os_cmd, "umount", mnt / "boot"])
    check_call([*os_cmd, "umount", mnt])


if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    main()
