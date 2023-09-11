#!/usr/bin/env bash

firo="$HOME/.firo/bin/firo"

theme=$1

uptime="`uptime -s`"

shutdown='󰐥'
reboot='󰜉'
lock='󰌾'
suspend='󰤄'
logout='󰗼'
yes='󰄬'
no=''

rofi_cmd() {
	rofi -dmenu \
		-p "Encendido desde $uptime" \
		-mesg "Encendido desde $uptime" \
		-theme ${theme}
}

confirm_cmd() {
	rofi -theme-str 'window {location: center; anchor: center; fullscreen: false; width: 350px;}' \
		-theme-str 'mainbox {children: [ "message", "listview" ];}' \
		-theme-str 'listview {columns: 2; lines: 1;}' \
		-theme-str 'element-text {horizontal-align: 0.5;}' \
		-theme-str 'textbox {horizontal-align: 0.5;}' \
		-dmenu \
		-p 'Confirmation' \
		-mesg '¿Continuar?' \
		-theme ${theme}
}

confirm_exit() {
	echo -e "$yes\n$no" | confirm_cmd
}

run_rofi() {
	echo -e "$lock\n$suspend\n$logout\n$reboot\n$shutdown" | rofi_cmd
}

execute_cmd() {
	selected="$(confirm_exit)"
	if [[ "$selected" == "$yes" ]]; then
		if [[ $1 == 'shutdown' ]]; then
			$firo power shutdown
		elif [[ $1 == 'reboot' ]]; then
			$firo power reboot
		elif [[ $1 == 'suspend' ]]; then
			$firo power suspend
		elif [[ $1 == 'logout' ]]; then
			$firo power logout
		fi
	else
		exit 0
	fi
}

chosen="$(run_rofi)"
case ${chosen} in
    $shutdown)
		execute_cmd 'shutdown' 
        ;;
    $reboot)
		execute_cmd 'reboot'
        ;;
    $lock)
		# execute_cmd 'lock'
		$firo power lock
        ;;
    $suspend)
		execute_cmd 'suspend'
        ;;
    $logout)
		execute_cmd 'logout'
        ;;
esac