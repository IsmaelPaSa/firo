#!/usr/bin/python

#   
#   ███████╗██╗██╗      ██████╗ 
#   ██╔════╝██║██║     ██╔═══██╗
#   █████╗  ██║██║     ██║   ██║
#   ██╔══╝  ██║██║     ██║   ██║
#   ██║     ██║███████╗╚██████╔╝
#   ╚═╝     ╚═╝╚══════╝ ╚═════╝ 
#   

DISTINC_KEY = "color-"

# Expected as input...


# {
#     "background": "#281e1e",
#     "foreground": "#e6e5e0",
#     "cursor": "#e6e5e0"
#     "color0": "#281e1e",
#     "color1": "#D0B195",
#     "color2": "#A6C3B7",
#     "color3": "#D0C69E",
#     "color4": "#D3CAA5",
#     "color5": "#E9CAB6",
#     "color6": "#A6D3D5",
#     "color7": "#e6e5e0",
#     "color8": "#a1a09c",
#     "color9": "#D0B195",
#     "color10": "#A6C3B7",
#     "color11": "#D0C69E",
#     "color12": "#D3CAA5",
#     "color13": "#E9CAB6",
#     "color14": "#A6D3D5",
#     "color15": "#e6e5e0"
# }

# All functions return a list

def mk_hypr_dot(name: str, value: str):
    return f"${DISTINC_KEY}{name}\t=\trgb({value.replace('#', '')})"

def mk_kitty_dot(name: str, value: str):
    return f"{name}\t{value}"

def mk_kss_dot(name: str, value: str):
    return f"@define-color\t{name}\t{value};"

def mk_less_dot(name: str, value: str):
    return f"@{name}:\t{value};"

def mk_rofi_dot(name: str, value: str):
    return f"{name}:\t{value};"

def mk_all(colors: dict):
    hypr = []
    kitty = []
    kss = []
    rofi = ["* {"]
    less = []

    for key, value in colors.items():
        hypr.append(mk_hypr_dot(key, value))
        kitty.append(mk_kitty_dot(key, value))
        kss.append(mk_kss_dot(key, value))
        less.append(mk_less_dot(key, value))
        rofi.append(mk_rofi_dot(key, value))
    
    rofi.append("}")

    return {
        "hypr": hypr,
        "kitty": kitty,
        "kss": kss,
        "rofi": rofi,
        "less": less
    }