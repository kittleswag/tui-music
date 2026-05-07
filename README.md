tui-music
Показывает текст песен из Spotify прямо в терминале. Слова появляются по одному с плавной анимацией — как караоке, только без музыки.
Работает в любом терминале. Я тестировал в Kitty на Hyprland, всё летает.
Как установить
Клонируй репозиторий:
git clone https://github.com/kittleswag/tui-music.git
cd tui-music
Создай виртуальное окружение и установи зависимости:
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Как запустить
python main.py
Что внутри

    main.py — запускает всё

    renderer.py — отвечает за анимацию и отрисовку

    spotify.py — подтягивает текущий трек из Spotify

    lyrics.py — ищет текст песни

