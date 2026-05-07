import requests
from bs4 import BeautifulSoup
import re
import urllib.parse

def get_lyrics_from_genius(artist, title):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    # Формируем URL для azlyrics.com
    # Формат: https://www.azlyrics.com/lyrics/artist/song.html
    artist_clean = re.sub(r'[^a-zA-Z0-9]', '', artist).lower()
    title_clean = re.sub(r'[^a-zA-Z0-9]', '', title).lower()
    
    url = f"https://www.azlyrics.com/lyrics/{artist_clean}/{title_clean}.html"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Ищем основной div с текстом
            main_div = soup.find('div', class_='col-xs-12 col-lg-8 text-center')
            if main_div:
                # Текст находится после "Usage of azlyrics.com..."
                text_div = main_div.find('div', class_=None, style=None)
                if not text_div:
                    # Ищем любой div без класса
                    for div in main_div.find_all('div'):
                        if not div.get('class'):
                            text_div = div
                            break
                
                if text_div:
                    # Очищаем от лишнего
                    text = text_div.get_text(separator='\n')
                    # Убираем строки с рекламой
                    lines = [line.strip() for line in text.split('\n') 
                            if line.strip() and 'azlyrics' not in line.lower()]
                    return '\n'.join(lines)
    except:
        pass
    
    return None
