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
import argparse
import subprocess
import os
import json

import f_colors as firo_colors

BACKGROUND_FILE = "~/.firo/assets/background"
DIRS_FILE = "~/.firo/config/dirs.json"
THEMES_FILE = "~/.firo/config/theme.json"

COLORS_FOLDER = "~/.firo/assets/colors/"
HYRP_COLOR_FILE = COLORS_FOLDER + "hypr.conf"
KITTY_COLOR_FILE = COLORS_FOLDER + "kitty.conf"
KSS_COLOR_FILE = COLORS_FOLDER + "kss.css"
ROFI_COLOR_FILE = COLORS_FOLDER + "rofi.rasi"
LESS_COLOR_FILE = COLORS_FOLDER + "less.less"
JSON_COLOR_FILE = COLORS_FOLDER + "colors.json"

WALLPAPER_SCRIPT = "~/.firo/core/scripts/set-wallpaper.sh"
KILL_N_RELOAD_SCRIPT = "~/.firo/core/scripts/kill-n-reload.sh"
THEME_SCRIPT = "~/.firo/core/scripts/set-theme.sh"

WAL_JSON_COLOR_FILE = "~/.cache/wal/colors.json"

REQUEST_COPY = [
    {
        "from": KSS_COLOR_FILE,
        "to": "waybar",
        "as": "colors.css"
    },
    {
        "from": KSS_COLOR_FILE,
        "to": "swaync",
        "as": "colors.css"
    }
]

def expand(path: str):
    return os.path.abspath(os.path.expanduser(path))

def copy_file(source: str, dest: str):
    shutil.copy(expand(source), expand(dest))

def copy_dir(source: str, dest: str):
    shutil.copytree(expand(source), expand(dest))

def load_json(path: str):
    with open(path, "r") as my_json:
        return json.load(my_json)

def write_json(path: str, data: dict):
    with open(path, "w") as my_json:
        json.dump(data, my_json, indent = 4)

def write_lines(path:str, lines: list):
    with open(path, "w") as my_file:
        for line in lines:
            my_file.write(f"{line}\n")

def exec_cmd(cmd: str):
    subprocess.run(
        cmd,
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

BACKGROUND_FILE = expand(BACKGROUND_FILE)
DIRS_FILE = expand(DIRS_FILE)
THEMES_FILE = expand(THEMES_FILE)
COLORS_FOLDER = expand(COLORS_FOLDER)
HYRP_COLOR_FILE = expand(HYRP_COLOR_FILE)
KITTY_COLOR_FILE = expand(KITTY_COLOR_FILE)
KSS_COLOR_FILE = expand(KSS_COLOR_FILE)
ROFI_COLOR_FILE = expand(ROFI_COLOR_FILE)
LESS_COLOR_FILE = expand(LESS_COLOR_FILE)
JSON_COLOR_FILE = expand(JSON_COLOR_FILE)
WALLPAPER_SCRIPT = expand(WALLPAPER_SCRIPT)
WAL_JSON_COLOR_FILE = expand(WAL_JSON_COLOR_FILE)
KILL_N_RELOAD_SCRIPT = expand(KILL_N_RELOAD_SCRIPT)
THEME_SCRIPT = expand(THEME_SCRIPT)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Background and Color Manager")
    parser.add_argument("background", type=str, help="Background path")
    parser.add_argument("-l", "--light", action="store_true")
    args = parser.parse_args()

    USR_BACKGROUND = expand(args.background)

    copy_file(args.background, BACKGROUND_FILE)
    exec_cmd(f"{WALLPAPER_SCRIPT} '{USR_BACKGROUND}' {'-l' if args.light else ''}")
    
    dirs = load_json(DIRS_FILE)
    themes = load_json(THEMES_FILE)

    pre_colors_json = load_json(WAL_JSON_COLOR_FILE)
    colors_json = {}
    
    for key, value in pre_colors_json["special"].items():
        colors_json[key] = value
    for key, value in pre_colors_json["colors"].items():
        colors_json[key] = value

    generated_colors = firo_colors.mk_all(colors_json)
    
    write_lines(HYRP_COLOR_FILE, generated_colors["hypr"])
    write_lines(KITTY_COLOR_FILE, generated_colors["kitty"])
    write_lines(KSS_COLOR_FILE, generated_colors["kss"])
    write_lines(ROFI_COLOR_FILE, generated_colors["rofi"])
    write_lines(LESS_COLOR_FILE, generated_colors["less"])
    write_json(JSON_COLOR_FILE, colors_json)

    for request in REQUEST_COPY:
        copy_file(
            request["from"],
            dirs["config"][request["to"]] + request["as"]
        )

    exec_cmd(f"{KILL_N_RELOAD_SCRIPT}")
    
    exec_cmd(f"{THEME_SCRIPT} {themes['gtk']['light' if args.light else 'dark'] } {themes['kvantum']['light' if args.light else 'dark']} {'-l' if args.light else ''}")