#!/bin/bash

SLEEP_TIME=0.01
PERCENTAGE_SKIPS=10
BRIGHT_SKIPS=1

set_bright_percentage() {
    percentage=$1
    mode=$2
    if [ "$mode" = true ]; then
        brightnessctl -q s "+${percentage}%"
    else
        brightnessctl -q s "${percentage}%-"
    fi
}

smooth_bright() {
    skips=$1
    mode=$2
    for ((i = 0; i < skips; i++)); do
        set_bright_percentage $BRIGHT_SKIPS $mode
        sleep $SLEEP_TIME
    done
}

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <action>"
    exit 1
fi

case "$1" in
    "inc")
        smooth_bright $PERCENTAGE_SKIPS true
        ;;
    "dec")
        smooth_bright $PERCENTAGE_SKIPS false
        ;;
    *)
        echo "Invalid action"
        exit 1
        ;;
esac
