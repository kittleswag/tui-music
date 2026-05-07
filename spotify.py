import subprocess
import requests
import time

# Токен Spotify (получим автоматически)
_TOKEN = None
_TOKEN_TIME = 0

def _get_token():
    global _TOKEN, _TOKEN_TIME
    if _TOKEN and time.time() - _TOKEN_TIME < 3600:
        return _TOKEN
    
    # Получаем токен из Spotify Web Player
    url = "https://open.spotify.com/get_access_token?reason=transport&productType=web_player"
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    if r.status_code == 200:
        _TOKEN = r.json()['accessToken']
        _TOKEN_TIME = time.time()
        return _TOKEN
    return None

def _run(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, text=True).strip()
    except subprocess.CalledProcessError:
        return None

def is_running():
    status = _run("playerctl status")
    return status is not None

def get_metadata():
    meta = _run("playerctl metadata --format '{{artist}} - {{title}}'")
    return meta

def get_position():
    pos = _run("playerctl position")
    try:
        return float(pos)
    except:
        return 0.0

def get_status():
    return _run("playerctl status")

def get_lyrics_from_spotify(artist, title):
    token = _get_token()
    if not token:
        return None
    
    # Ищем трек
    headers = {'Authorization': f'Bearer {token}'}
    query = f"{artist} {title}"
    r = requests.get(f'https://api.spotify.com/v1/search?q={query}&type=track&limit=1', headers=headers)
    
    if r.status_code == 200:
        tracks = r.json()['tracks']['items']
        if tracks:
            track_id = tracks[0]['id']
            # Получаем текст через расширенный API Spotify
            r2 = requests.get(f'https://spclient.wg.spotify.com/color-lyrics/v2/track/{track_id}', 
                            headers={'Authorization': f'Bearer {token}'})
            if r2.status_code == 200:
                lyrics_data = r2.json()
                if 'lyrics' in lyrics_data:
                    return lyrics_data['lyrics']['lines']
    return None
