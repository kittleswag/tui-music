import time
import traceback

from spotify import *
from lyrics import *
from renderer import Renderer

OFFSET = 0.25


def main():
    renderer = Renderer()

    current_track = None
    words = []
    index = 0

    while True:

        if not is_running():
            renderer.draw_message("Spotify is not running")
            time.sleep(1)
            continue

        track = get_metadata()

        if track != current_track:
            current_track = track
            renderer.draw_message(f"Loading: {track}")

            lrc = fetch_lyrics(track)

            if not lrc:
                renderer.draw_message("No synced lyrics found")
                words = []
                index = 0
                time.sleep(2)
                continue

            lines = parse_lrc(lrc)
            words = expand_words(lines)
            index = 0

        if get_status() == "Paused":
            time.sleep(0.05)
            continue

        pos = get_position() + OFFSET

        if words and index < len(words) - 1:
            if pos >= words[index + 1]["time"]:
                index += 1

        if words:
            renderer.draw_word(words[index]["word"], intensity=1.0)

        time.sleep(0.008)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        input("Press Enter...")