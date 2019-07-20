#!/usr/bin/env bash

# pylint: disable=missing-docstring

from subprocess import check_call, call
from typing import NamedTuple, List, Optional
import argparse
import logging

LOG = logging.getLogger(__name__)

LUKS_PADDING_MB = 20


class Partition(NamedTuple):
    name: str
    file_system: str
    size_mb: Optional[int]
    is_boot: bool = False


def main():
    parser = argparse.ArgumentParser("partitions")
    parser.add_argument(
        "--mode", choices=["simple", "crypt", "crypt-double"], required=True
    )
    parser.add_argument("--device", type=str, required=True)
    parser.add_argument("--main-size-mb", type=int, default=None)
    parser.add_argument("--perm-size-mb", type=int, default=None)
    parser.add_argument("--boot-size-mb", type=int, default=256)
    parser.add_argument("--swap-size-mb", type=int, default=256)
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
            args.main_size_mb is not None
        ), "--main-size-mb must be specified for crypt-double"
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
    crypt_base(device, boot_size_mb)
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
    crypt_base(device, boot_size_mb)
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

def crypt_base(device: str, boot_size_mb: int) -> None:
    make_partitions(
        device,
        [
            Partition("boot", "ext4", boot_size_mb, is_boot=True),
            Partition("luks", "ext4", None),
        ],
    )


def make_partitions(device: str, partitions: List[Partition]) -> None:
    verify_partition_sizes(partitions)

    LOG.info("Making partitions on %s", device)
    parted(device, "mklabel gpt")
    # TODO: why start at 1mb?
    written_to_mb = 1
    for i, partition in enumerate(partitions):
        LOG.info("Making partition on %s: %s", device, partition)
        start_str = f"{written_to_mb}MiB"
        end_str = (
            f"{written_to_mb + partition.size_mb}MiB"
            if partition.size_mb is not None
            else "100%"
        )
        parted(
            device,
            f"mkpart primary {partition.file_system} {start_str} {end_str}",
        )
        if partition.is_boot:
            LOG.info("Setting as boot on %s: %s", device, partition)
            parted(device, f"set {i + 1} esp on")
        if partition.size_mb is None:
            LOG.info("Partition filled rest of space, finishing")
            break
        written_to_mb += partition.size_mb
    parted(device, "print")


def make_luks_partitions(
    device: str, luks_name: str, partitions: List[Partition]
) -> None:
    verify_partition_sizes(partitions)

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
        size_cmd = (
            ["--size", f"{partition.size_mb}M"]
            if partition.size_mb is not None
            else ["--extents", "100%FREE"]
        )
        check_call(
            [
                "lvcreate",
                *size_cmd,
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
        if partition.size_mb is None:
            LOG.info("Partition filled rest of space, finishing")
            break


def parted(device: str, command: str) -> None:
    check_call(["parted", device, "--script", *command.split(" ")])


def verify_partition_sizes(partitions: List[Partition]) -> None:
    assert all(
        partition.size_mb is not None for partition in partitions[:-1]
    ), f"Only the last partition can not specify size, got: {partitions}"
    total_mb = sum(
        partition.size_mb
        for partition in partitions
        if partition.size_mb is not None
    )
    LOG.info("Total partition size will be %dMiB", total_mb)


if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    main()
