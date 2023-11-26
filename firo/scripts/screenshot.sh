#!/bin/bash 

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <action>"
    exit 1
fi

case "$1" in
    "window")
        hyprshot -m window
        ;;
    "screen")
        hyprshot -m output
        ;;
    "region")
        hyprshot -m region
        ;;
    *)
        exit 0
        ;;
esac
