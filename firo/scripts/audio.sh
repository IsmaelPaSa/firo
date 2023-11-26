#!/bin/bash 

SLEEP_TIME=0.01
PERCENTAGE_SKIPS=5
VOLUME_SKIPS=1

toggle_mute() {
    device=$1
    wpctl set-mute $device toggle
}

set_volume_percentage() {
    device=$1
    percentage=$2
    mode=$3
    if [ "$mode" = true ]; then
        wpctl set-volume $device "${percentage}%+"
    else
        wpctl set-volume $device "${percentage}%-"
    fi
}

smooth_volume() {
    device=$1
    skips=$2
    mode=$3
    wpctl set-mute $device 0
    for ((i = 0; i < skips; i++)); do
        set_volume_percentage $device $VOLUME_SKIPS $mode
        sleep $SLEEP_TIME
    done
}

actman() {
    device=$1
    action=$2
    case "$action" in
        "inc")
            smooth_volume $device $PERCENTAGE_SKIPS true
            ;;
        "dec")
            smooth_volume $device $PERCENTAGE_SKIPS false
            ;;
        "mute")
            toggle_mute $device
            ;;
        *)
            exit 0
            ;;
    esac
}

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <device> <action>"
    exit 1
fi

case "$1" in
    "mic")
        actman @DEFAULT_SOURCE@ $2
        ;;
    "speaker")
        actman @DEFAULT_AUDIO_SINK@ $2
        ;;
    *)
        exit 0
        ;;
esac
