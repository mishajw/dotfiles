#!/usr/bin/env python

"""
Quickly run, format, and edit files.

For example, you can start editing a file:
    quick.py edit foo.rs

...format it:
    quick.py fmt foo.rs

...and then run it:
    quick.py run foo.rs

See init_handlers for supported file types.
"""

from pathlib import Path
from typing import Callable
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
import argparse
import os
import subprocess
import sys


PYTHON = os.environ["DF_PYTHON"]
EDITOR = os.environ.get("EDITOR", "vim")
HOME = os.environ["HOME"]

PathPrerequisite = Callable[[Path], bool]
Command = List[str]
CommandsGenerator = Callable[[Path], List[Command]]
FileTemplate = str

run_handlers: List[Tuple[PathPrerequisite, CommandsGenerator]] = []
fmt_handlers: List[Tuple[PathPrerequisite, CommandsGenerator]] = []
edit_handlers: List[Tuple[PathPrerequisite, FileTemplate]] = []


def init_handlers() -> None:
    def has_ext(extension: str) -> PathPrerequisite:
        return lambda path: path.suffix == ("." + extension)

    def is_cargo(path: Path) -> bool:
        return has_ext("rs")(path) and Path("Cargo.toml").is_file()

    def path_command(*args) -> CommandsGenerator:
        return lambda path: [[*args, str(path)]]

    def command(*args) -> CommandsGenerator:
        return lambda _: [list(args)]

    def build_and_run_rs(path: Path) -> List[Command]:
        return [["rustc", path, "-o", "/tmp/quick.out"], ["/tmp/quick.out"]]

    is_py = has_ext("py")
    run_handlers.append((is_py, path_command(PYTHON)))
    fmt_handlers.append((is_py, path_command(PYTHON, "-m", "black", "--line-length", 100)))
    edit_handlers.append((is_py, '#!/usr/bin/env python\nprint("Hello, world!")'))

    run_handlers.append((is_cargo, command("cargo", "run")))
    fmt_handlers.append((is_cargo, command("cargo", "fmt")))

    is_rs = has_ext("rs")
    run_handlers.append((is_rs, build_and_run_rs))
    fmt_handlers.append((is_rs, path_command("rustfmt")))
    edit_handlers.append((is_rs, 'fn main() { println!("Hello, world!"); }',))

    is_sh = has_ext("sh")
    run_handlers.append((is_sh, path_command()))
    fmt_handlers.append((is_sh, path_command("shfmt", "-w", "-i", "2")))


def get_handler(path: Path, handlers: List[Tuple[PathPrerequisite, Any]], default=None) -> Any:
    for prerequisite, handler in handlers:
        if prerequisite(path):
            return handler
    if default is not None:
        return default
    print(f"Unsupported file type: {path}")
    sys.exit()


def exec_commands(commands: List[Command]) -> None:
    assert len(commands) > 0, "Must have at least one command."
    assert all(len(command) > 0 for command in commands), "Command must not be empty."
    commands = [[str(arg) for arg in command] for command in commands]

    *commands, last_command = commands
    for command in commands:
        subprocess.check_call(command)
    os.execlp(last_command[0], *last_command)


def edit_with_template(path: Path, file_template: FileTemplate) -> None:
    if not path.is_file():
        path.write_text(file_template)
    exec_commands([[EDITOR, path]])


if __name__ == "__main__":
    parser = argparse.ArgumentParser("quick")
    parser.add_argument("--scratch-dir", type=str, default=Path(HOME) / "src" / "scratch")
    subparsers = parser.add_subparsers(dest="command", help="commands")

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("path")

    fmt_parser = subparsers.add_parser("fmt")
    fmt_parser.add_argument("paths", nargs="+")

    edit_parser = subparsers.add_parser("edit")
    edit_parser.add_argument("path")
    edit_parser.add_argument("--scratch", action="store_true")

    args = parser.parse_args()
    init_handlers()

    if args.command == "run":
        path = Path(args.path)
        print(f"Running {path}")
        commands = get_handler(path, run_handlers)(path)
        exec_commands(commands)
    elif args.command == "fmt":
        for path in args.paths:
            path = Path(path)
            print(f"Formatting {path}")
            commands = get_handler(Path(path), fmt_handlers)(path)
            exec_commands(commands)
    elif args.command == "edit":
        path = Path(args.path)
        if args.scratch:
            path = Path(args.scratch_dir) / path
        file_template = get_handler(path, edit_handlers, default="")
        print(f"Editing {path}")
        edit_with_template(path, file_template)
    else:
        raise AssertionError()
