#!/bin/bash

TO_RELOAD=(
    "waybar"
    "neofetch"
)

TO_REFRESH=(
    "swaync-client -rs"
    "neofetch --clean"
    "kitty @ set-colors --all --configured ~/.firo/colors/kitty.conf"
)

kill_n_restart() {
    task=$1
    killall $task
    $task &
}

only_restart() {
    task=$1
    $task &
}

if [ "$#" -ne 0 ]; then
    echo "Usage: $0"
    exit 1
fi

for k_task in "${TO_RELOAD[@]}"; do
    kill_n_restart "$k_task"
done
for r_task in "${TO_REFRESH[@]}"; do
    only_restart "$r_task"
done
