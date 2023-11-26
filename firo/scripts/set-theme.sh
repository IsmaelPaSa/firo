#!/bin/bash

GTK_DARK_MODE=prefer-dark
GTK_LIGHT_MODE=default

if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <theme-gtk> <theme-kvantum> [-l]"
    exit 1
fi

if [ "$3" = "-l" ]; then
    gtk_mode=$GTK_LIGHT_MODE
else
    gtk_mode=$GTK_DARK_MODE
fi

kvantummanager --set $2

gsettings set org.gnome.desktop.interface gtk-theme $1

gsettings set org.gnome.desktop.interface color-scheme $gtk_mode