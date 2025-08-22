#!/usr/bin/python3
# ⚙️ НАСТРОЙКИ ZADARMA DOWNLOADER
# ==============================
# Конфигурационный файл для настройки API ключей и параметров работы

import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# 🔑 ЗАDARMA API КЛЮЧИ
# Получите в личном кабинете: https://my.zadarma.com/api/
# Используем переменные окружения с fallback значениями для разработки
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# 🌍 РЕЖИМ РАБОТЫ
# False = Production (боевой режим)
# True = Sandbox (тестовый режим)
SANDBOX_MODE = os.getenv("SANDBOX_MODE", "False").lower() == "true"

# 📅 НАСТРОЙКИ ВРЕМЕНИ
# Количество дней назад для поиска записей
DAYS_BACK = int(os.getenv("DAYS_BACK", "1"))  # По умолчанию: последние 24 часа

# 📁 НАСТРОЙКИ ПАПОК
# Папка для сохранения аудиофайлов (относительно корня проекта)
DOWNLOAD_FOLDER = os.getenv("DOWNLOAD_FOLDER", "downloads")

# 🎵 НАСТРОЙКИ ФАЙЛОВ
# Формат имени файла (можно изменить)
# Доступные переменные: {call_id}, {date}, {time}, {sip}, {destination}, {duration}
FILENAME_TEMPLATE = os.getenv("FILENAME_TEMPLATE", "call_{call_id}_{date}_{time}_{sip}_to_{destination}.wav")

# 🔧 ТЕХНИЧЕСКИЕ НАСТРОЙКИ
# Таймаут для HTTP запросов (в секундах)
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "60"))

# Максимальное количество попыток скачивания файла
MAX_DOWNLOAD_ATTEMPTS = int(os.getenv("MAX_DOWNLOAD_ATTEMPTS", "3"))

# 📊 НАСТРОЙКИ ЛОГИРОВАНИЯ
# Уровень детализации логов
# DEBUG = максимальная детализация
# INFO = обычные сообщения
# WARNING = только предупреждения и ошибки
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Сохранять ли логи в файл
SAVE_LOGS_TO_FILE = os.getenv("SAVE_LOGS_TO_FILE", "True").lower() == "true"
LOG_FILE = os.getenv("LOG_FILE", "logs/zadarma_downloader.log")
