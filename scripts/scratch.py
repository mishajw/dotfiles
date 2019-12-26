#!/usr/bin/env python

from pathlib import Path
import argparse
import os
import re

"""
Creates scratch files for quick notes.
"""

DEFAULT_PY = """
#!/usr/bin/env python
print("Hello, world!")
"""
DEFAULT_RS = """
fn main() {
    println!("Hello, world!");
}
"""

parser = argparse.ArgumentParser("scratch")
parser.add_argument("name", type=str, default=".md")
parser.add_argument("--dir", type=str, default=Path(os.environ["HOME"]) / "src" / "scratch")
args = parser.parse_args()

scratch_dir = Path(args.dir)
scratch_name = args.name
editor = os.environ["EDITOR"]

# If only extension is supplied, then default to "scratch".
if re.match(r"\.[^\.]*", scratch_name):
    scratch_name = "scratch" + scratch_name

if not scratch_dir.is_dir():
    scratch_dir.mkdir(parents=True)
scratch_path = scratch_dir / scratch_name

if not scratch_path.is_file():
    if scratch_path.suffix == ".py":
        contents = DEFAULT_PY
    elif scratch_path.suffix == ".rs":
        contents = DEFAULT_RS
    else:
        contents = ""
    contents = contents.strip()
    scratch_path.write_text(contents)

os.execlp(editor, editor, scratch_path)
