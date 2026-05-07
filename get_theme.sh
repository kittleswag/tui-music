#!/bin/bash
# Ищем активную тему через include в kitty.conf
theme_line=$(grep "^include" ~/.config/kitty/kitty.conf 2>/dev/null | head -1)
if [ -n "$theme_line" ]; then
    theme_path=$(echo "$theme_line" | awk '{print $2}')
    basename "$theme_path" .conf
else
    echo "deepseek"
fi
