#!/usr/bin/python

#   
#   ███████╗██╗██╗      ██████╗ 
#   ██╔════╝██║██║     ██╔═══██╗
#   █████╗  ██║██║     ██║   ██║
#   ██╔══╝  ██║██║     ██║   ██║
#   ██║     ██║███████╗╚██████╔╝
#   ╚═╝     ╚═╝╚══════╝ ╚═════╝ 
#   

import shutil
import sys
import os
import json
import subprocess
from distutils.dir_util import copy_tree

# Utils
def expand(path: str):
    return os.path.abspath(os.path.expanduser(path))

def copy_file(source: str, dest: str):
    shutil.copy(expand(source), expand(dest))

def copy_dir(source: str, dest: str):
    copy_tree(expand(source), expand(dest))

def mk_config_path(name: str):
    source = DOTFILES_FOLDER + name + "/"
    dest = CONFIG_FOLDERS[name]
    return source, dest 

def exec_cmd(cmd: str):
    subprocess.run(
        cmd,
        shell=True
    )

# Main
if __name__ == "__main__":
    # Check OS
    if sys.platform != 'linux':
        print("Linux Only!")
        sys.exit(1)

    # Read JSONs
    with open("config/dirs.json", "r") as config_dirs_json:
        dirs = json.load(config_dirs_json)
    with open("setup/packages.json", "r") as setup_packages_json:
        packages = json.load(setup_packages_json)

    FIRO_FOLDER = "~/.firo/"
    CONFIG_FOLDERS = dirs["config"]
    CURRENT_FOLDER = os.path.dirname(__file__) + "/"
    DOTFILES_FOLDER = CURRENT_FOLDER + "setup/dotfiles/"

    FIRO_BIN_CMD = "~/.firo/bin/firo"
    FIRO_WALLPAPER_CMD = "wallpaper"
    INITIAL_WALLPAPER_FILE = "~/.firo/setup/wallpaper.jpg"

    CHMOD_CMD = "chmod -R +x"
    CHSH_CMD = "chsh $USER -s $(which zsh)"
    SUDO_CMD = packages["sudo"]

    # Copy Firo Folder
    copy_dir(CURRENT_FOLDER, FIRO_FOLDER)

    # Copy Single Config
    for folder in CONFIG_FOLDERS:
        copy_dir(*mk_config_path(folder))

    # Executable permissions
    exec_cmd(f"{CHMOD_CMD} {FIRO_FOLDER}")

    # Set initial background
    exec_cmd(f"{expand(FIRO_BIN_CMD)} {FIRO_WALLPAPER_CMD} {expand(INITIAL_WALLPAPER_FILE)}")

    # Switch to zsh
    exec_cmd(f"{CHSH_CMD}")