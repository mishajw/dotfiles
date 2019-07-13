#!/usr/bin/env bash

# pylint: disable=missing-docstring

import argparse
import subprocess
import logging
from typing import NamedTuple, List

LOG = logging.getLogger(__name__)


class Partition(NamedTuple):
    file_system: str
    size_mb: int
    is_boot: bool = False


def main():
    parser = argparse.ArgumentParser("partitions")
    parser.add_argument("--device", type=str, required=True)
    parser.add_argument("--main-size-mb", type=int, required=True)
    parser.add_argument("--boot-size-mb", type=int, default=256)
    parser.add_argument("--swap-size-mb", type=int, default=256)
    args = parser.parse_args()

    make_partitions(
        args.device,
        [
            Partition("ext4", args.boot_size_mb, is_boot=True),
            Partition("linux-swap", args.swap_size_mb),
            Partition("ext4", args.main_size_mb),
        ],
    )


def make_partitions(device: str, partitions: List[Partition]) -> None:
    parted(device, "mklabel gpt")
    # TODO: why start at 1mb?
    written_to_mb = 1
    for i, partition in enumerate(partitions):
        LOG.info("Making partition on %s: %s", device, partition)
        start_mb = written_to_mb
        end_mb = start_mb + partitions.size_mb
        parted(
            device,
            f"mkpart primary {partition.file_system} {start_mb}MiB {end_mb}Mib",
        )
        written_to_mb = end_mb
        if partition.is_boot:
            LOG.info("Setting as boot on %s: %s", device, partition)
            parted(device, f"set {i + 1} esp on")
    parted(device, "print")


def parted(device: str, command: str) -> None:
    subprocess.check_call(["parted", device, *command.split(" ")])


if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    main()
