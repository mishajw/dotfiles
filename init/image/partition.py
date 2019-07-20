#!/usr/bin/env bash

# pylint: disable=missing-docstring

from subprocess import check_call, call
from typing import NamedTuple, List
import argparse
import logging

LOG = logging.getLogger(__name__)

LUKS_PADDING_MB = 20


class Partition(NamedTuple):
    name: str
    file_system: str
    size_mb: int
    is_boot: bool = False


def main():
    parser = argparse.ArgumentParser("partitions")
    parser.add_argument(
        "--mode", choices=["simple", "crypt", "crypt-double"], required=True
    )
    parser.add_argument("--device", type=str, required=True)
    parser.add_argument("--main-size-mb", type=int, required=True)
    parser.add_argument("--boot-size-mb", type=int, default=256)
    parser.add_argument("--swap-size-mb", type=int, default=256)
    parser.add_argument("--perm-size-mb", type=int, default=None)
    parser.add_argument("--luks-name", type=str, default="luks")
    args = parser.parse_args()

    # Clean up from previous runs
    if call(["cryptsetup", "status", "cryptlvm"]) == 0:
        LOG.info("Closing cryptlvm")
        call(["vgchange", "--activate", "n", args.luks_name])
        check_call(["cryptsetup", "close", "cryptlvm"])

    if args.mode == "simple":
        simple(
            args.device, args.main_size_mb, args.boot_size_mb, args.swap_size_mb
        )
    elif args.mode == "crypt":
        crypt(
            args.device,
            args.luks_name,
            args.main_size_mb,
            args.boot_size_mb,
            args.swap_size_mb,
        )
    elif args.mode == "crypt-double":
        assert (
            args.perm_size_mb is not None
        ), "--perm-size-mb must be specified for crypt-double"
        crypt_double(
            args.device,
            args.luks_name,
            args.main_size_mb,
            args.perm_size_mb,
            args.boot_size_mb,
            args.swap_size_mb,
        )
    else:
        raise AssertionError()


def simple(
    device: str, main_size_mb: int, boot_size_mb: int, swap_size_mb: int
):
    make_partitions(
        device,
        [
            Partition("boot", "ext4", boot_size_mb, is_boot=True),
            Partition("swap", "linux-swap", swap_size_mb),
            Partition("main", "ext4", main_size_mb),
        ],
    )


def crypt(
    device: str,
    luks_name: str,
    main_size_mb: int,
    boot_size_mb: int,
    swap_size_mb: int,
):
    make_partitions(
        device,
        [
            Partition("boot", "ext4", boot_size_mb, is_boot=True),
            Partition(
                "luks", "ext4", swap_size_mb + main_size_mb + LUKS_PADDING_MB
            ),
        ],
    )

    make_luks_partitions(
        f"{device}p2",
        luks_name,
        [
            Partition("swap", "linux-swap", swap_size_mb),
            Partition("main", "ext4", main_size_mb),
        ],
    )

def crypt_double(
    device: str,
    luks_name: str,
    main_size_mb: int,
    perm_size_mb: int,
    boot_size_mb: int,
    swap_size_mb: int,
):
    make_partitions(
        device,
        [
            Partition("boot", "ext4", boot_size_mb, is_boot=True),
            Partition(
                "luks", "ext4", swap_size_mb + main_size_mb + LUKS_PADDING_MB
            ),
        ],
    )

    make_luks_partitions(
        f"{device}p2",
        luks_name,
        [
            Partition("swap", "linux-swap", swap_size_mb),
            Partition("main-a", "ext4", main_size_mb),
            Partition("main-b", "ext4", main_size_mb),
            Partition("perm", "ext4", perm_size_mb),
        ],
    )


def make_partitions(device: str, partitions: List[Partition]) -> None:
    LOG.info("Making partitions on %s", device)
    parted(device, "mklabel gpt")
    # TODO: why start at 1mb?
    written_to_mb = 1
    for i, partition in enumerate(partitions):
        LOG.info("Making partition on %s: %s", device, partition)
        start_mb = written_to_mb
        end_mb = start_mb + partition.size_mb
        parted(
            device,
            f"mkpart primary {partition.file_system} {start_mb}MiB {end_mb}Mib",
        )
        written_to_mb = end_mb
        if partition.is_boot:
            LOG.info("Setting as boot on %s: %s", device, partition)
            parted(device, f"set {i + 1} esp on")
    parted(device, "print")


def make_luks_partitions(
    device: str, luks_name: str, partitions: List[Partition]
) -> None:
    LOG.info("Setting up cryptlvm on %s", device)
    check_call(["cryptsetup", "luksFormat", device])
    LOG.info("Opening cryptlvm")
    check_call(["cryptsetup", "open", device, "cryptlvm"])
    LOG.info("Initializing physical volume")
    check_call(["pvcreate", "-ff", "/dev/mapper/cryptlvm"])
    LOG.info("Initializing volume group")
    check_call(["vgcreate", luks_name, "/dev/mapper/cryptlvm"])
    for partition in partitions:
        LOG.info("Making encrypted partition on %s: %s", device, partition)
        check_call(
            [
                "lvcreate",
                "--size",
                f"{partition.size_mb}M",
                luks_name,
                "--name",
                partition.name,
            ]
        )
        if partition.file_system == "ext4":
            LOG.info("Making ext4")
            check_call(["mkfs.ext4", f"/dev/{luks_name}/{partition.name}"])
        elif partition.file_system == "linux-swap":
            LOG.info("Making swap")
            check_call(["mkswap", f"/dev/{luks_name}/{partition.name}"])
        else:
            raise AssertionError()


def parted(device: str, command: str) -> None:
    check_call(["parted", device, "--script", *command.split(" ")])


if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    main()
