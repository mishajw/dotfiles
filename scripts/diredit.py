#!/usr/bin/env python3

from typing import Dict, List
import argparse
import glob
import os
import subprocess
import tempfile

DEFAULT_EDITOR = "vim"

Files = Dict[int, str]


class Action:
    def run(self) -> None:
        raise NotImplementedError()

    def description(self) -> str:
        raise NotImplementedError()


class Rename(Action):
    def __init__(self, original_path, new_path):
        self.original_path = original_path
        self.new_path = new_path

    def run(self) -> None:
        assert os.path.isfile(self.original_path)

        new_directory_name = os.path.dirname(self.new_path)
        if not os.path.isdir(new_directory_name):
            os.mkdir(new_directory_name)

        os.rename(self.original_path, self.new_path)

    def description(self) -> str:
        return f"Rename {self.original_path} -> {self.new_path}"


class Delete(Action):
    def __init__(self, path: str):
        self.path = path

    def run(self) -> None:
        assert os.path.isfile(self.path), f"Can't find file {self.path}"
        os.remove(self.path)

    def description(self) -> str:
        return f"Delete {self.path}"


def main():
    parser = argparse.ArgumentParser("dredit")
    parser.add_argument("--directory", type=str, default=None)
    parser.add_argument("--editor", type=str, default=None)

    # Get arguments
    args = parser.parse_args()
    directory = args.directory
    if directory is None:
        directory = os.getcwd()

    editor = args.editor
    if editor is None:
        if "EDITOR" in os.environ:
            editor = os.environ["EDITOR"]
        else:
            editor = DEFAULT_EDITOR

    files: Files = __get_files(directory)
    initial_text: str = __files_to_text(files)

    edited_text = __get_edited_text(initial_text, editor)
    edited_files = __text_to_files(edited_text)

    actions = __get_actions(files, edited_files)

    if len(actions) == 0:
        return

    print("Will perform:")
    for a in actions:
        print(a.description())

    continue_response = input("Continue? [Y/n] ")
    continue_response = continue_response.lower().strip()
    should_continue = continue_response == "" or continue_response == "y"

    if should_continue:
        print("Performing actions")
        for a in actions:
            a.run()
    else:
        print("Not performing actions")


def __get_edited_text(initial_text: str, editor: str) -> str:
    with tempfile.NamedTemporaryFile() as editor_file:
        # Write the directory contents
        editor_file.write(initial_text.encode())
        editor_file.flush()

        # Show editor to user
        subprocess.call([editor, editor_file.name])

        # Read the file back in
        editor_file.seek(0)
        return editor_file.read().decode()


def __files_to_text(files: Files) -> str:
    return "\n".join([f"{i}: {files[i]}" for i in files])


def __text_to_files(text: str) -> Files:
    def files_iter():
        for line in text.split("\n"):
            if line.strip() == "":
                continue

            try:
                index, file_path = line.split(":")
                index = int(index)
                yield (index, file_path.strip())
            except ValueError as e:
                print(line, e)

    return dict(files_iter())


def __get_files(directories: str) -> Files:
    files = glob.iglob(os.path.join(directories, "**"), recursive=True)
    files = [f for f in files if os.path.isfile(f)]
    return dict(enumerate(files))


def __get_actions(original: Files, edited: Files) -> List[Action]:
    all_keys = set()
    all_keys.update(original.keys())
    all_keys.update(edited.keys())

    def actions_iter():
        for key in all_keys:
            if key in original and key in edited:
                if original[key] != edited[key]:
                    yield Rename(original[key], edited[key])
            elif key in original and key not in edited:
                yield Delete(original[key])
            else:
                raise ValueError(f"Unrecognized index {key}")

    return list(actions_iter())


if __name__ == "__main__":
    main()
