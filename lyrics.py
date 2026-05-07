import requests
import re
import time
import unicodedata

CACHE = {}

def normalize(text):
    # Убираем диакритику: é → e, ô → o
    nfkd = unicodedata.normalize('NFKD', text)
    return nfkd.encode('ASCII', 'ignore').decode('ASCII')

def fetch_lyrics(query):
    if query in CACHE:
        return CACHE[query]

    # Пробуем оригинальный запрос
    result = _try_fetch(query)
    if result:
        CACHE[query] = result
        return result

    # Если не вышло — пробуем нормализовать
    if ' - ' in query:
        artist, title = query.split(' - ', 1)
        artist_norm = normalize(artist)
        title_norm = normalize(title)
        
        if artist_norm != artist or title_norm != title:
            clean_query = f"{artist_norm} - {title_norm}"
            result = _try_fetch(clean_query)
            if result:
                CACHE[query] = result
                return result

    return None

def _try_fetch(query):
    url = "https://lrclib.net/api/search"
    params = {"q": query}
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        r = requests.get(url, params=params, headers=headers, timeout=10)
        if r.status_code != 200:
            return None

        data = r.json()
        for item in data:
            synced = item.get('syncedLyrics', '')
            if synced and len(synced.strip()) > 50:
                return synced
            plain = item.get('plainLyrics', '')
            if plain and len(plain.strip()) > 50:
                return plain
    except:
        pass

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
        plain_lines = [l.strip() for l in lrc_text.splitlines() if l.strip()]
        for i, line in enumerate(plain_lines):
            lines.append((i * 3.0, line))

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
