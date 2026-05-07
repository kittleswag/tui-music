import sys
import shutil
import time
import math
import subprocess
import json


def get_kitty_colors():
    try:
        out = subprocess.check_output(["kitty", "@", "get-colors"], text=True)
        data = json.loads(out)
        fg = data.get("foreground", "#ffffff")
        return fg
    except:
        return "#eeeeee"


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


class Renderer:
    def __init__(self):
        self.current_word = ""
        self.word_start = 0

        self.fg_hex = get_kitty_colors()
        self.fr, self.fg_, self.fb = hex_to_rgb(self.fg_hex)

        sys.stdout.write("\033[2J")
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

    def _size(self):
        return shutil.get_terminal_size(fallback=(80, 24))

    def _move(self, x, y):
        sys.stdout.write(f"\033[{y};{x}H")

    def _clear(self):
        sys.stdout.write("\033[2J")

    def _color(self, r, g, b, a=1.0):
        r = int(r * a)
        g = int(g * a)
        b = int(b * a)
        return f"\033[38;2;{r};{g};{b}m"

    # 🌊 smooth flow background (НЕ точки)
    def draw_background(self, t):
        cols, rows = self._size()

        for y in range(1, rows, 2):
            for x in range(1, cols, 2):

                n = math.sin(x * 0.05 + t) + math.cos(y * 0.04 + t)

                if n > 0.6:
                    char = " "
                elif n > 0.2:
                    char = "·"
                else:
                    char = "."

                alpha = 0.10 + (n + 2) * 0.08

                self._move(x, y)
                sys.stdout.write(
                    self._color(self.fr, self.fg_, self.fb, alpha) + char
                )

    # 🎵 main word render
    def draw_word(self, word, intensity=1.0):
        cols, rows = self._size()
        now = time.time()

        if word != self.current_word:
            self.current_word = word
            self.word_start = now

        self._clear()

        # фон
        self.draw_background(now)

        # fade-in
        t = (now - self.word_start) / 0.12
        t = max(0.0, min(1.0, t))

        # bounce
        bounce = math.sin(t * math.pi) * 1.5

        x = (cols - len(word)) // 2
        y = rows // 2 + int(bounce * 0.2)

        alpha = max(0.3, t)

        # мягкий glow от темы kitty
        glow = 0.9 + 0.2 * intensity

        self._move(x, y)
        sys.stdout.write(
            self._color(self.fr, self.fg_, self.fb, alpha) + word
        )

        sys.stdout.flush()

    def draw_message(self, text):
        cols, rows = self._size()

        self._clear()

        x = (cols - len(text)) // 2
        y = rows // 2

        self._move(x, y)
        sys.stdout.write(self._color(self.fr, self.fg_, self.fb, 1.0) + text)
        sys.stdout.flush()