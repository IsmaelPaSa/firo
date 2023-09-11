#!/bin/bash

#   
#   ███████╗██╗██╗      ██████╗ 
#   ██╔════╝██║██║     ██╔═══██╗
#   █████╗  ██║██║     ██║   ██║
#   ██╔══╝  ██║██║     ██║   ██║
#   ██║     ██║███████╗╚██████╔╝
#   ╚═╝     ╚═╝╚══════╝ ╚═════╝ 
#   

WAL_FOLDER="$HOME/.cache/wal/"

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <image_path> [-i]"
    exit 1
fi

killall swaybg
swaybg -m fill -i "$1" &

if [ "$2" = "-l" ]; then
    wal -i "$1" -l
    pywalfox light
else
    wal -i "$1"
    pywalfox dark
fi


pywalfox update
