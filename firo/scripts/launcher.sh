#!/bin/bash

LAUNCHER_FOLDER="$HOME/.firo/launchers/"

# name.sh and name.rasi is required in launchers/ folder

MENU_LAUNCHER="$LAUNCHER_FOLDER""menu"
POWER_LAUNCHER="$LAUNCHER_FOLDER""power"

launch() {
    path="$1"
    "$path.sh" "$path.rasi"
}

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <action>"
    exit 1
fi

case "$1" in
    "menu")
        launch "$MENU_LAUNCHER"
        ;;
    "power")
        launch "$POWER_LAUNCHER"
        ;;
    *)
        exit 0
        ;;
esac
