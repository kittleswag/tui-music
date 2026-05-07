import requests
import re
import time

CACHE = {}


def fetch_lyrics(query):
    if query in CACHE:
        return CACHE[query]

    url = "https://lrclib.net/api/search"
    params = {"q": query}

    for _ in range(3):
        try:
            r = requests.get(url, params=params, timeout=5)
            data = r.json()

            for item in data:
                if item.get("syncedLyrics"):
                    CACHE[query] = item["syncedLyrics"]
                    return item["syncedLyrics"]

            return None
        except:
            time.sleep(1)

    return None


def parse_lrc(lrc_text):
    pattern = r"\[(\d+):(\d+\.\d+)\](.*)"
    lines = []

    for line in lrc_text.splitlines():
        m = re.match(pattern, line)
        if not m:
            continue

        minutes = int(m.group(1))
        seconds = float(m.group(2))
        text = m.group(3).strip()

        t = minutes * 60 + seconds
        lines.append((t, text))

    return lines


def expand_words(lines):
    words = []

    for i in range(len(lines)):
        t, text = lines[i]
        next_t = lines[i + 1][0] if i + 1 < len(lines) else t + 3

        parts = text.split()
        if not parts:
            continue

        step = (next_t - t) / len(parts)

        for j, word in enumerate(parts):
            words.append({
                "time": t + j * step,
                "word": word
            })

    return words