#!/bin/bash
kitty_theme=$(readlink ~/.config/kitty/kitty.conf)
if [ -z "$kitty_theme" ]; then
    echo "deepseek"
else
    basename "$kitty_theme" .conf
fi
