#!/usr/bin/env python
from pathlib import Path

import subprocess

_SYMLINKS: dict[str, Path] = {
    ".vimrc": Path("~/.vimrc"),
    ".gitconfig": Path("~/.gitconfig"),
    "yabairc": Path("~/.yabairc"),
    "skhdrc": Path("~/.skhdrc"),
    "vscode-settings.json": Path(
        "~/Library/Application Support/Code/User/settings.json"
    ),
}


def main():
    create_symlinks()
    install_oh_my_zsh()
    source_setup_script_in_zsh()


def create_symlinks() -> None:
    log("Creating symlinks")
    for src, dst in _SYMLINKS.items():
        src = Path(__file__).resolve().parent / "config" / src
        dst = dst.expanduser()
        log(f"{src} -> {dst}")

        if not dst.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.symlink_to(src)
            log("> created")
            continue

        if not dst.is_symlink():
            log("> ERROR: normal file exists at symlink dst")
            continue

        current_link = dst.resolve()
        if current_link != src:
            log(
                f"> ERROR: symlink exists, but points to {current_link} "
                f"(expected {src})"
            )
            continue

        log("> already exists")


def source_setup_script_in_zsh():
    log("Sourcing setup script in ~/.zshrc")
    zshrc = Path("~/.zshrc").expanduser()

    if not zshrc.exists():
        zshrc.touch()
    assert zshrc.is_file()

    source_text = f"source {Path(__file__).resolve().parent / 'setup_shell.sh'}"
    if source_text in zshrc.read_text():
        log("> setup script already sourced")
        return

    with open(zshrc, "a") as f:
        f.write(f"\n{source_text}\n")
    log("> sourced")


def install_oh_my_zsh():
    log("Installing Oh My Zsh and plugins")
    confirmation = input("Do you want to install Oh My Zsh and plugins? (y/n): ").lower()
    if confirmation != "y":
        log("> Oh My Zsh and plugins installation skipped")
        return
    install_script = """
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" unattended
    git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
    git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
    git clone https://github.com/joshskidmore/zsh-fzf-history-search ${ZSH_CUSTOM:=~/.oh-my-zsh/custom}/plugins/zsh-fzf-history-search
    """

    subprocess.run(install_script, shell=True, check=True, executable='/bin/bash')
    log("> Oh My Zsh and plugins installed successfully")

def log(s: str) -> None:
    print(f"\033[32m[mishajw/dotfiles]\033[39m {s}")


if __name__ == "__main__":
    main()
