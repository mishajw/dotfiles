#!/usr/bin/env python

"""
Runs a file.
"""

from pathlib import Path
import argparse
import os
import subprocess
import sys

parser = argparse.ArgumentParser("dfrun")
parser.add_argument("mode", type=str, choices=["run", "format"])
parser.add_argument("path", type=str)
parser.add_argument("--compile-file", type=str, default="/tmp/dfrun.out")
args = parser.parse_args()

path = Path(args.path)
compile_file = Path(args.compile_file)
df_python = os.environ["DF_PYTHON"]

if args.mode == "run":
    if path.suffix == ".py":
        os.execl(df_python, df_python, path)
    elif path.suffix == ".rs" and Path("Cargo.toml").is_file():
        os.execlp("cargo", "cargo", "run")
    elif path.suffix == ".rs":
        subprocess.check_output(["rustc", path, "-o", compile_file])
        os.execlp(compile_file, compile_file)
    elif path.suffix == ".sh":
        os.execlp(path, path)
elif args.mode == "format":
    if path.suffix == ".py":
        os.execl(df_python, df_python, "-m", "black", path)
    elif path.suffix == ".rs" and Path("Cargo.toml").is_file():
        os.execlp("cargo", "cargo", "format")
    elif path.suffix == ".rs":
        os.execlp("rustfmt", "rustfmt", path)
    elif path.suffix == ".sh":
        os.execlp("shfmt", "shfmt", "-w", "-i", "2", path)
else:
    print(f"Unrecognized extension for {mode}: {path}")
    sys.exit(1)
