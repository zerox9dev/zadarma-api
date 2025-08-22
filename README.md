# Zadarma Audio Downloader

## Задача
Нужно было скачивать аудиозаписи звонков из Zadarma API за последние 24 часа.

## Установка

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

2. Создайте файл `.env` на основе `.env.example`:
   ```bash
   cp .env.example .env
   ```

3. Настройте переменные окружения в файле `.env`:
   ```bash
   API_KEY=ваш_api_ключ
   API_SECRET=ваш_api_секрет
   ```

## Использование

1. Убедитесь, что настроены переменные окружения в `.env`
2. Запустите: `python3 run.py`
3. Файлы сохраняются в `downloads/`

## Переменные окружения

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `API_KEY` | API ключ Zadarma | `your_api_key_here` |
| `API_SECRET` | API секрет Zadarma | `your_api_secret_here` |
| `SANDBOX_MODE` | Режим песочницы (true/false) | `False` |
| `DAYS_BACK` | Количество дней назад для поиска | `1` |
| `DOWNLOAD_FOLDER` | Папка для сохранения файлов | `downloads` |
| `FILENAME_TEMPLATE` | Шаблон имени файла | `call_{call_id}_{date}_{time}_{sip}_to_{destination}.wav` |
| `REQUEST_TIMEOUT` | Таймаут HTTP запросов (сек) | `60` |
| `MAX_DOWNLOAD_ATTEMPTS` | Максимум попыток скачивания | `3` |
| `LOG_LEVEL` | Уровень логирования | `INFO` |
| `SAVE_LOGS_TO_FILE` | Сохранять логи в файл (true/false) | `True` |
| `LOG_FILE` | Путь к файлу логов | `logs/zadarma_downloader.log` |

## Структура
```
zadarma-downloader/
├── run.py              # Запуск
├── config/settings.py  # Настройки
├── src/downloader.py   # Логика
├── src/zadarma/api.py  # API клиент
├── requirements.txt    # Зависимости
├── .env.example       # Пример переменных окружения
└── .env               # Ваши переменные окружения (не в git)
```

Работает стабильно, скачивает аудиофайлы с правильными именами.