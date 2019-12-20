#!/usr/bin/env python

from pathlib import Path
import argparse
import os

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
parser.add_argument("language", type=str, choices=["py", "rs", "md"])
parser.add_argument("name", type=str, nargs="?", default="scratch")
parser.add_argument("--dir", type=str, default=Path(os.environ["HOME"]) / "src" / "scratch")
args = parser.parse_args()

language = args.language
scratch_name = args.name
scratch_dir = Path(args.dir)
scratch_path = scratch_dir / (scratch_name + "." + language)
editor = os.environ["EDITOR"]

if not scratch_dir.is_dir():
    scratch_dir.mkdir(parents=True)

if not scratch_path.is_file():
    if language == "py":
        contents = DEFAULT_PY
    elif language == "rs":
        contents = DEFAULT_RS
    else:
        contents = ""
    contents = contents.strip()
    scratch_path.write_text(contents)

os.execlp(editor, editor, scratch_path)
