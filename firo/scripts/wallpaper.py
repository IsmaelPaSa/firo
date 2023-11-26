#!/usr/bin/python

import shutil
import argparse
import subprocess
import os
import json
from colorthief import ColorThief
import colorsys
import math

def _mk_hypr_dot(name: str, value: str):
    return f"$color-{name} = rgb({value.replace('#', '')})"

def _mk_kitty_dot(name: str, value: str):
    return f"{name} {value}"

def _mk_kss_dot(name: str, value: str):
    return f"@define-color {name} {value};"

def _mk_less_dot(name: str, value: str):
    return f"@{name}: {value};"

def _mk_rofi_dot(name: str, value: str):
    return f"{name}: {value};"

def mk_firo_colors(colors: dict):
    hypr = []
    kitty = []
    kss = []
    rofi = ["* {"]
    less = []

    for key, value in colors.items():
        semicolon_key = key.replace("_", "-")
        hypr.append(_mk_hypr_dot(key, value))
        kitty.append(_mk_kitty_dot(key, value))
        kss.append(_mk_kss_dot(key, value))
        less.append(_mk_less_dot(key, value))
        rofi.append(_mk_rofi_dot(semicolon_key, value))
    
    rofi.append("}")

    return {
        "hypr": hypr,
        "kitty": kitty,
        "kss": kss,
        "rofi": rofi,
        "less": less
    }

def pywal_color_mapper(colors, wallpaper):
    return {
        "alpha": "100",
        "wallpaper": wallpaper,
        "special": {
            "background": colors["background"],
            "foreground": colors["foreground"],
            "cursor": colors["cursor"]
        },
        "colors": {
            "color0": colors["color0"],
            "color1": colors["color1"],
            "color2": colors["color2"],
            "color3": colors["color3"],
            "color4": colors["color4"],
            "color5": colors["color5"],
            "color6": colors["color6"],
            "color7": colors["color7"],
            "color8": colors["color8"],
            "color9": colors["color9"],
            "color10": colors["color10"],
            "color11": colors["color11"],
            "color12": colors["color12"],
            "color13": colors["color13"],
            "color14": colors["color14"],
            "color15": colors["color15"]
        }
    }

def _rgb_to_hex(red, green, blue):
    return '#%02x%02x%02x' % (red, green, blue)

def _get_color_palette(src: str, quantity: int, quality: int):
    color_thief = ColorThief(src)
    return color_thief.get_palette(color_count=quantity, quality=quality)

def _sort_by_hsv(color):
    hsv_color = colorsys.rgb_to_hsv(color[0] / 255.0, color[1] / 255.0, color[2] / 255.0)
    return hsv_color[1], 1 - hsv_color[2]

def _sort_by_bright(color):
    hsv_color = colorsys.rgb_to_hls(color[0] / 255.0, color[1] / 255.0, color[2] / 255.0)
    return hsv_color[2]

def _sort_by_dom(color):
    return max(enumerate(color), key=lambda x: x[1])[0]

def _sort_by_saturation(color):
    hsv_color = colorsys.rgb_to_hsv(color[0] / 255.0, color[1] / 255.0, color[2] / 255.0)
    return (1 - hsv_color[1]) * hsv_color[2]

def _euc_distance(color_one, color_two):
    return math.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(color_one, color_two)))

def _get_whittest_and_darskest(colors):
    white = (255, 255, 255)
    black = (0, 0, 0)
    wnd = {}
    wnd["whittest"] = min(colors, key=lambda color: _euc_distance(color, white))
    wnd["darkest"] = min(colors, key=lambda color: _euc_distance(color, black))
    return wnd

def mk_color_palette(sauce: str, white_mode=True):
    color_quantity = 24
    color_quality = 16
    colors = _get_color_palette(sauce, color_quantity, color_quality)
    
    by_hsv = sorted(colors, key=_sort_by_hsv)
    by_bright = sorted(colors, key=_sort_by_bright)
    by_saturation = sorted(colors, key=_sort_by_saturation)
    by_dom = sorted(colors, key=_sort_by_dom)
    wnd = _get_whittest_and_darskest(colors)
    
    final = {}

    def popman(to_pop):
        try:
            by_hsv.remove(to_pop)
        except:
            pass
        try:
            by_bright.remove(to_pop)
        except:
            pass
        try:
            by_saturation.remove(to_pop)
        except:
            pass
        try:
            by_dom.remove(to_pop)
        except:
            pass

    fc = {}
    if white_mode:
        

        fc["background"] = by_saturation[-1]
        fc["foreground"] = wnd['darkest']
        fc["cursor"] = fc["foreground"]


        popman(fc["background"])
        popman(fc["foreground"])
        popman(by_bright[-1])
        popman(by_saturation[-1])
        

        fc["color7"] = wnd['darkest']
        fc["color15"] = fc["color7"]
        fc["color0"] = fc["background"]
        fc["color8"] = by_hsv[0]

        popman(fc["color8"])
        
        for i in range(1, 4):
            fc[f"color{i}"] = by_hsv[int(f"-{i}")]
            fc[f"color{i+8}"] = fc[f"color{i}"]
            fc[f"color{i+3}"] = by_dom[int(f"{i}")]
            fc[f"color{i+8+3}"] = fc[f"color{i+3}"]
    else: 


        fc["background"] = by_saturation[0]
        fc["foreground"] = by_saturation[-1]
        fc["cursor"] = fc["foreground"]


        popman(fc["background"])
        popman(fc["foreground"])
        popman(wnd["darkest"])
        

        fc["color7"] = wnd["whittest"]
        fc["color15"] = fc["color7"]
        fc["color0"] = fc["background"]
        fc["color8"] = by_hsv[0]

        popman(fc["color8"])
        popman(fc["color7"])

        for i in range(int(color_quantity/3)):
            popman(by_bright[0])
        for i in range(1, 4):
            fc[f"color{i}"] = by_hsv[-1]
            fc[f"color{i+8}"] = fc[f"color{i}"]
            popman(fc[f"color{i}"])
            fc[f"color{i+3}"] = by_saturation[-1]
            fc[f"color{i+8+3}"] = fc[f"color{i+3}"]
            popman(fc[f"color{i+3}"])

    fc["selection_foreground"] = fc["background"]
    fc["selection_background"] = fc["foreground"]

    for key, value in fc.items():
        final[key] = _rgb_to_hex(*value)
    return final

def expand(path: str):
    return os.path.abspath(os.path.expanduser(path))

def exec_cmd(cmd: str):
    subprocess.run(
        cmd,
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def load_json(path: str):
    with open(path, "r") as json_file:
        data = json.load(json_file)
    return data

def write_json(path: str, data: dict):
    with open(path, "w") as my_json:
        json.dump(data, my_json, indent = 4)

def write_lines(path:str, lines: list):
    with open(path, "w") as my_file:
        for line in lines:
            my_file.write(f"{line}\n")

def copy_file(source: str, dest: str):
    shutil.copy(source, dest)

parser = argparse.ArgumentParser(
    description="Firo Wallpaper Manager Script",
    epilog="Thanks for using Firo!",
    allow_abbrev=False
)
parser.add_argument("background", type=str, help="Background path")
parser.add_argument("-l", "--light", action="store_true")
args = parser.parse_args()

FIRO_FOLDER = expand("~/.firo/") + "/"

FIRO_WALLPAPER_FILE = FIRO_FOLDER + "wallpaper"
FIRO_THEME_FILE = FIRO_FOLDER + "config/theme.json"

COLORS_FOLDER = FIRO_FOLDER +  "colors/"
HYRP_COLOR_FILE = COLORS_FOLDER + "hypr.conf"
KITTY_COLOR_FILE = COLORS_FOLDER + "kitty.conf"
KSS_COLOR_FILE = COLORS_FOLDER + "kss.css"
ROFI_COLOR_FILE = COLORS_FOLDER + "rofi.rasi"
LESS_COLOR_FILE = COLORS_FOLDER + "less.less"
JSON_COLOR_FILE = COLORS_FOLDER + "colors.json"
PYWAL_COLOR_FILE = COLORS_FOLDER + "pywal.json"

SCRIPTS_FOLDER = FIRO_FOLDER + "scripts/"
WALLPAPER_SCRIPT = SCRIPTS_FOLDER + "set-wallpaper.sh"
THEME_SCRIPT = SCRIPTS_FOLDER + "set-theme.sh"
RELOAD_SCRIPT = SCRIPTS_FOLDER + "do-reload.sh"

WAL_JSON_COLOR_FILE = expand("~/.cache/wal/colors.json")
SWAYNC_COLOR_FILE = expand("~/.config/swaync/colors.css")
WAYBAR_COLOR_FILE = expand("~/.config/waybar/colors.css")

REQUEST_COPY = [
    {
        "from": KSS_COLOR_FILE,
        "to": SWAYNC_COLOR_FILE
    },
    {
        "from": KSS_COLOR_FILE,
        "to": WAYBAR_COLOR_FILE
    }
]

if __name__ == "__main__":
    USR_BACKGROUND = expand(args.background)
    LIGHT_MODE = args.light
    copy_file(USR_BACKGROUND, FIRO_WALLPAPER_FILE)
    exec_cmd(f"{WALLPAPER_SCRIPT} '{FIRO_WALLPAPER_FILE}' {'-l' if LIGHT_MODE else ''}")
    
    colors_json = mk_color_palette(USR_BACKGROUND, LIGHT_MODE)
    generated_colors = mk_firo_colors(colors_json)

    write_lines(HYRP_COLOR_FILE, generated_colors["hypr"])
    write_lines(KITTY_COLOR_FILE, generated_colors["kitty"])
    write_lines(KSS_COLOR_FILE, generated_colors["kss"])
    write_lines(ROFI_COLOR_FILE, generated_colors["rofi"])
    write_lines(LESS_COLOR_FILE, generated_colors["less"])
    write_json(JSON_COLOR_FILE, colors_json)
    write_json(PYWAL_COLOR_FILE, pywal_color_mapper(colors_json, USR_BACKGROUND))

    for request in REQUEST_COPY:
        copy_file(
            request["from"],
            request["to"]
        )
    
    copy_file(PYWAL_COLOR_FILE, WAL_JSON_COLOR_FILE)
    
    themes = load_json(FIRO_THEME_FILE)
    exec_cmd(f"{THEME_SCRIPT} {themes['gtk']['light' if LIGHT_MODE else 'dark'] } {themes['kvantum']['light' if LIGHT_MODE else 'dark']} {'-l' if LIGHT_MODE else ''}")
    
    exec_cmd(f"{RELOAD_SCRIPT}")