#!/usr/bin/python3
# 🚀 ZADARMA DOWNLOADER - ЗАПУСК
# =============================
#
# Главный файл для запуска скачивания аудиозаписей.
#
# Использование:
#     python3 run.py
#
# Перед запуском настройте API ключи в config/settings.py

import sys
import os

# Добавляем путь к модулям
sys.path.append(os.path.dirname(__file__))

from src.downloader import main

if __name__ == "__main__":
    main()
