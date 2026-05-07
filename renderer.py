import sys
import shutil
import time
import math
import json
import subprocess
import os

THEMES_FILE = os.path.join(os.path.dirname(__file__), "themes.json")
GET_THEME_SCRIPT = os.path.join(os.path.dirname(__file__), "get_theme.sh")

def load_theme():
    try:
        theme_name = subprocess.check_output([GET_THEME_SCRIPT], text=True).strip()
        with open(THEMES_FILE) as f:
            themes = json.load(f)
        return themes.get(theme_name, themes["deepseek"])
    except:
        return {"primary": "#4a8cf7", "secondary": "#7aaff7", "text": "#e0e8f0"}

class Renderer:
    def __init__(self):
        self.current_word = ""
        self.start = time.time()
        print("\033[2J")
        print("\033[?25l")

    def size(self):
        return shutil.get_terminal_size()

    def move(self, x, y):
        print(f"\033[{y};{x}H", end="")

    def clear(self):
        print("\033[2J")

    def draw_word(self, word):
        theme = load_theme()
        primary = theme["primary"]
        r, g, b = int(primary[1:3], 16), int(primary[3:5], 16), int(primary[5:7], 16)
        
        cols, rows = self.size()
        now = time.time()

        if word != self.current_word:
            self.current_word = word
            self.start = now

        self.clear()

        t = min(1, (now - self.start) / 0.15)
        bounce = int(math.sin(t * math.pi) * 2)

        x = (cols - len(word)) // 2
        y = rows // 2 + bounce

        self.move(x, y)
        print(f"\033[38;2;{r};{g};{b}m{word}\033[0m", end="")

        sys.stdout.flush()
