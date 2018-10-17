#!/usr/bin/env python3.6

from typing import List, Optional
import argparse
import os
import subprocess

FALLBACK_EDITOR = "vim"
FALLBACK_SHELL = "vim"

def main(
        path: str,
        exec_indicator: str,
        editor: Optional[str],
        shell: Optional[str]) -> None:
    edit_file(path, editor)
    commands = get_commands(path, exec_indicator)
    print("Executing commands:\n%s" % "\n".join(commands))
    exec_commands(commands, shell)
    strip_exec_indicator(path, exec_indicator)

def edit_file(path: str, editor: Optional[str]):
    editor = resolve(editor, "EDITOR", FALLBACK_EDITOR)
    subprocess.run([editor, path], check=True)

def get_commands(path: str, exec_indicator: str) -> List[str]:
    with open(path, "r") as f:
        return [
            line[len(exec_indicator):-1]
            for line in f
            if line.startswith(exec_indicator)]

def exec_commands(commands: List[str], shell: Optional[str]) -> None:
    shell = resolve(shell, "SHELL", FALLBACK_SHELL)
    subprocess.run([shell, "-c", "\n".join(commands)])

def strip_exec_indicator(path: str, exec_indicator: str) -> None:
    with open(path, "r") as f:
        stripped_lines = [
            line[len(exec_indicator):]
                if line.startswith(exec_indicator)
                else line
            for line in f]
    with open(path, "w") as f:
        for line in stripped_lines:
            f.write(line)

def resolve(optional: Optional[str], env_name: str, fallback: str) -> str:
    if optional:
        return optional
    if env_name in os.environ:
        return os.environ[env_name]
    return fallback

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute commands from a file")
    parser.add_argument("path", type=str, help="File containing commands")
    parser.add_argument("--exec-indicator", type=str, default="> ")
    parser.add_argument("--editor", type=str, default=None)
    parser.add_argument("--shell", type=str, default=None)
    args = parser.parse_args()
    main(args.path, args.exec_indicator, args.editor, args.shell)
