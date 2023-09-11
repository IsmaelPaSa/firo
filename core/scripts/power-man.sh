#!/bin/bash

#   
#   ███████╗██╗██╗      ██████╗ 
#   ██╔════╝██║██║     ██╔═══██╗
#   █████╗  ██║██║     ██║   ██║
#   ██╔══╝  ██║██║     ██║   ██║
#   ██║     ██║███████╗╚██████╔╝
#   ╚═╝     ╚═╝╚══════╝ ╚═════╝ 
#   

LOCK_CMD="swaylock"
SHUTDOWN_CMD="shutdown -h now"
REBOOT_CMD="reboot"
LOGOUT_CMD="hyprctl dispatch exit"
SUSPEND_CMD="systemctl suspend"

execute() {
    cmd="$1"
    $cmd
}

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <action>"
    exit 1
fi

case "$1" in
    "lock")
        execute "$LOCK_CMD"
        ;;
    "suspend")
        execute "$SUSPEND_CMD"
        ;;
    "reboot")
        execute "$REBOOT_CMD"
        ;;
    "shutdown")
        execute "$SHUTDOWN_CMD"
        ;;
    "logout")
        execute "$LOGOUT_CMD"
        ;;
    *)
        exit 0
        ;;
esac
