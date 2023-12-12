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

def pywal_json_color_mapper(colors, wallpaper):
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

def pywal_colors_color_mapper(colors):
    return [
        colors["color0"],
        colors["color1"],
        colors["color2"],
        colors["color3"],
        colors["color4"],
        colors["color5"],
        colors["color6"],
        colors["color7"],
        colors["color8"],
        colors["color9"],
        colors["color10"],
        colors["color11"],
        colors["color12"],
        colors["color13"],
        colors["color14"],
        colors["color15"]
    ]
#####



def _rgb_to_hex(red, green, blue):
    return '#%02x%02x%02x' % (red, green, blue)

def _get_color_palette(src: str, quantity: int, quality: int):
    color_thief = ColorThief(src)
    return color_thief.get_palette(color_count=quantity, quality=quality)

def _get_color_luminance(color: tuple):
    normalized_color = [c / 255.0 for c in color]
    return 0.2126 * normalized_color[0] + 0.7152 * normalized_color[1] + 0.0722 * normalized_color[2]

def _get_color_hsv(color: tuple):
    hsv_color = colorsys.rgb_to_hsv(color[0] / 255.0, color[1] / 255.0, color[2] / 255.0)
    return hsv_color[0], hsv_color[1], hsv_color[2]

def _get_color_hsv_hue(color: tuple):
    return _get_color_hsv(color)[0]

def _get_color_hsv_saturation(color: tuple):
    return _get_color_hsv(color)[1]

def _get_color_hsv_value(color: tuple):
    return _get_color_hsv(color)[2]

def _get_color_saturation(color):
    hsv_color = colorsys.rgb_to_hsv(color[0] / 255.0, color[1] / 255.0, color[2] / 255.0)
    return (1 - hsv_color[1]) * hsv_color[2]

def _get_color_dominance(color):
    return max(enumerate(color), key=lambda x: x[1])[0]

def _get_color_contrast(color_foreground: tuple, color_background: tuple):
    def luminance(value):
        value /= 255.0
        if value <= 0.03928:
            return value / 12.92
        else:
            return ((value + 0.055) / 1.055) ** 2.4

    luminance_text = 0.2126 * luminance(color_foreground[0]) + 0.7152 * luminance(color_foreground[1]) + 0.0722 * luminance(color_foreground[2])
    luminance_background = 0.2126 * luminance(color_background[0]) + 0.7152 * luminance(color_background[1]) + 0.0722 * luminance(color_background[2])

    contrast = abs(luminance_text - luminance_background)
    return contrast

def _darken_color(color: tuple, factor: float):
    return tuple(int(c * (1 - factor)) for c in color)

def _lighten_color(color: tuple, factor: float):
   return tuple(int(c + (255 - c) * factor) for c in color)

def _get_readable_colors(colors: list, background_color: tuple, threshold: float):
    readable_colors = []
    unreadable_colors = []
    for color in colors:
        if _get_color_contrast(color, background_color) >= threshold:
            readable_colors.append(color)
        else:
            unreadable_colors.append(color)

    return readable_colors, unreadable_colors

'''
Base Components
'''

def _make_color_palette(sauce: str, mode: str, color_rules: dict):
    COLOR_QUANTITY = color_rules["quantity"]
    COLOR_QUALITY = color_rules["quality"]

    READABLE_ON_DARK_THRESHOLD = color_rules["readable"]["dark"]
    READABLE_ON_LIGHT_THRESHOLD = color_rules["readable"]["light"]

    IS_DARK_THRESHOLD = color_rules["is_dark"]
    IS_LIGHT_THRESHOLD =  color_rules["is_light"]

    DARKEN_FACTOR = color_rules["factor"]["darken"]
    LIGHTEN_FACTOR = color_rules["factor"]["lighten"]

    MIN_DIFFERENT_COLORS = 7

    SAME_DARK_RANGE = 5
    
    MODES = ["DARK", "LIGHT", "AUTO"]

    palette = _get_color_palette(sauce, COLOR_QUANTITY, COLOR_QUALITY)
    by_luminance = sorted(palette, key=_get_color_luminance)
    by_saturation = sorted(palette, key=_get_color_saturation)
    by_hsv_value = sorted(palette, key=_get_color_hsv_value)

    # To do: check mode when mode is AUTO
    IS_DARK = mode == "DARK" 

    lightest_color = by_saturation[-1]
    darkest_color = by_saturation[0] if IS_DARK else by_luminance[0]

    if IS_DARK:
        if not by_saturation[0] in by_hsv_value[:SAME_DARK_RANGE]:
            darkest_color = by_hsv_value[0]
    else:
        try:
            by_luminance.remove(by_hsv_value[-1])
        except:
            pass

    try:
        by_luminance.remove(lightest_color)
    except:
        pass
    try:
        by_luminance.remove(darkest_color)
    except:
        pass
    

    while True:
        darkest_color_luminance = _get_color_luminance(darkest_color)
        if darkest_color_luminance < IS_DARK_THRESHOLD:
            break
        darkest_color = _darken_color(darkest_color, DARKEN_FACTOR)
    while True:
        lightest_color_luminance = _get_color_luminance(lightest_color)
        if lightest_color_luminance > IS_LIGHT_THRESHOLD:
            break
        lightest_color = _lighten_color(lightest_color, LIGHTEN_FACTOR)

    background_color = darkest_color if IS_DARK else lightest_color
    foreground_color = lightest_color if IS_DARK else darkest_color

    readable_colors, unreadable_colors = _get_readable_colors(
        by_luminance,
        background_color,
        READABLE_ON_DARK_THRESHOLD if IS_DARK else READABLE_ON_LIGHT_THRESHOLD
    )

    # To do: make colors from unreadable 
    # while len(readable_colors) <= MIN_DIFFERENT_COLORS:
    #     pass



    by_hsv_saturation = sorted(readable_colors, key=_get_color_hsv_saturation)
    primary_colors = by_hsv_saturation
    if IS_DARK:
        by_hsv_value = sorted(readable_colors, key=_get_color_hsv_value, reverse=True)
        secondary_colors = by_hsv_value
    else:
        by_dominance = sorted(readable_colors, key=_get_color_dominance)
        secondary_colors = by_dominance

    by_hsv_hue = sorted(readable_colors, key=_get_color_hsv_hue)
    extra_colors = by_hsv_hue

    return {
        "background": background_color,
        "foreground": foreground_color,
        "cursor": foreground_color,
        "selection_foreground": background_color,
        "selection_background": foreground_color,
        "color0":   background_color, # Black
        "color8":   extra_colors[-1],

        "color1":   primary_colors[-1], # Red
        "color9":   primary_colors[-1], 
        "color2":   primary_colors[-2], # Green
        "color10":  primary_colors[-2],
        "color3":   primary_colors[-3], # Yellow
        "color11":  primary_colors[-3],
        "color4":   secondary_colors[0], # Blue
        "color12":  secondary_colors[0],
        "color5":   secondary_colors[1], # Magenta
        "color13":  secondary_colors[1],
        "color6":   secondary_colors[2], # Cyan
        "color14":  secondary_colors[2],
        
        "color7":   foreground_color, # White
        "color15":  extra_colors[0],
    }

def make_color_palette(sauce: str, mode: str):
    rules = {
        "quantity": 24,
        "quality": 16,
        "readable": {
            "dark": 0.0631,
            "light": 0.271
        },
        "is_dark": 0.333,
        "is_light": 0.666,
        "factor": {
            "darken": 0.1,
            "lighten": 0.1
        }
    }
    pre_color_palette = _make_color_palette(sauce, mode, rules)
    color_palette = {}
    for key in pre_color_palette:
        color_palette[key] = _rgb_to_hex(*pre_color_palette[key])
    return color_palette


#####

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
    dest_directory = os.path.dirname(dest)
    if not os.path.exists(dest_directory):
        os.makedirs(dest_directory)
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
WAL_COLORS_COLOR_FILE = expand("~/.cache/wal/colors")
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
    
    colors_json = make_color_palette(USR_BACKGROUND, "LIGHT" if LIGHT_MODE else "DARK")
    generated_colors = mk_firo_colors(colors_json)
    wal_json_colors_mapped = pywal_json_color_mapper(colors_json, USR_BACKGROUND)
    wal_colors_colors_mapped = pywal_colors_color_mapper(colors_json)

    write_lines(HYRP_COLOR_FILE, generated_colors["hypr"])
    write_lines(KITTY_COLOR_FILE, generated_colors["kitty"])
    write_lines(KSS_COLOR_FILE, generated_colors["kss"])
    write_lines(ROFI_COLOR_FILE, generated_colors["rofi"])
    write_lines(LESS_COLOR_FILE, generated_colors["less"])
    write_json(JSON_COLOR_FILE, colors_json)
    write_json(PYWAL_COLOR_FILE, wal_json_colors_mapped)
    write_lines(WAL_COLORS_COLOR_FILE, wal_colors_colors_mapped)

    for request in REQUEST_COPY:
        copy_file(
            request["from"],
            request["to"]
        )
    
    copy_file(PYWAL_COLOR_FILE, WAL_JSON_COLOR_FILE)
    
    themes = load_json(FIRO_THEME_FILE)
    exec_cmd(f"{THEME_SCRIPT} {themes['gtk']['light' if LIGHT_MODE else 'dark'] } {themes['kvantum']['light' if LIGHT_MODE else 'dark']} {'-l' if LIGHT_MODE else ''}")
    exec_cmd(f"{WALLPAPER_SCRIPT} '{FIRO_WALLPAPER_FILE}' {'-l' if LIGHT_MODE else ''}")
    exec_cmd(f"{RELOAD_SCRIPT}")