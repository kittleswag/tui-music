import requests
import re
import time

CACHE = {}

def fetch_lyrics(query):
    if query in CACHE:
        return CACHE[query]

    url = "https://lrclib.net/api/search"
    params = {"q": query}

    try:
        r = requests.get(url, params=params, timeout=10)
        if r.status_code == 200:
            data = r.json()
            
            # Проверяем каждый результат
            for item in data:
                synced = item.get("syncedLyrics", "")
                if synced and len(synced.strip()) > 50:
                    print(f"Found synced lyrics for {query}")
                    CACHE[query] = synced
                    return synced
            
            # Если нет синхронизированных, пробуем обычные
            for item in data:
                plain = item.get("plainLyrics", "")
                if plain and len(plain.strip()) > 50:
                    print(f"Found plain lyrics for {query}")
                    CACHE[query] = plain
                    return plain
    except Exception as e:
        print(f"Error fetching lyrics: {e}")

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

    if not lines:
        # Если нет синхронизированных строк, разбиваем текст на строки
        for i, line in enumerate(lrc_text.splitlines()):
            if line.strip():
                lines.append((i * 3.0, line.strip()))
    
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
