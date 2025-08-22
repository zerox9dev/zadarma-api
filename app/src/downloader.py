#!/usr/bin/python3
# 📥 ZADARMA AUDIO DOWNLOADER
# ===========================
#
# Основной модуль для скачивания аудиозаписей звонков из Zadarma API.

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from urllib.parse import urlparse

# Добавляем пути для импортов
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config.settings import *
from src.zadarma import api


class ZadarmaDownloader:
    # Класс для скачивания аудиозаписей из Zadarma
    
    def __init__(self):
        # Инициализация downloader'а
        self.api_client = api.ZadarmaAPI(
            key=API_KEY, 
            secret=API_SECRET, 
            sandbox=SANDBOX_MODE
        )
        self.download_folder = self._get_download_path()
        self.stats = {
            'found': 0,
            'downloaded': 0,
            'errors': 0
        }
    
    def _get_download_path(self):
        # Получение полного пути к папке для скачивания
        base_dir = os.path.dirname(os.path.dirname(__file__))
        return os.path.join(base_dir, DOWNLOAD_FOLDER)
    
    def _create_download_folder(self):
        # Создание папки для скачивания
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)
            self._log(f"📁 Создана папка: {self.download_folder}")
        else:
            self._log(f"📁 Используется папка: {self.download_folder}")
    
    def _log(self, message, level="INFO"):
        # Простое логирование
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def get_call_records(self):
        # Получение списка записей звонков
        self._log("🔍 Получаем список записей звонков...")
        
        # Вычисляем временной период
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=DAYS_BACK)
        
        date_from = start_time.strftime("%Y-%m-%d %H:%M:%S")
        date_to = end_time.strftime("%Y-%m-%d %H:%M:%S")
        
        self._log(f"📅 Период: {date_from} - {date_to}")
        
        try:
            # Запрос к API
            response_text = self.api_client.call('/v1/statistics/pbx/', {
                'start': date_from,
                'end': date_to
            })
            
            response = json.loads(response_text)
            
            if response.get('status') != 'success':
                raise Exception(f"API Error: {response.get('message', 'Unknown error')}")
            
            # Фильтруем звонки с записями
            all_calls = response.get('stats', [])
            recorded_calls = [call for call in all_calls if call.get('is_recorded') == 'true']
            
            self.stats['found'] = len(recorded_calls)
            
            self._log(f"📞 Всего звонков: {len(all_calls)}")
            self._log(f"🎵 Найдено записей: {len(recorded_calls)}")
            
            return recorded_calls
            
        except Exception as e:
            self._log(f"❌ Ошибка получения списка: {e}", "ERROR")
            return []
    
    def get_download_link(self, call_id):
        # Получение ссылки для скачивания записи
        try:
            response_text = self.api_client.call('/v1/pbx/record/request/', {
                'call_id': call_id
            })
            
            response = json.loads(response_text)
            
            if response.get('status') != 'success':
                self._log(f"⚠️ Не удалось получить ссылку для {call_id}: {response.get('message')}", "WARNING")
                return None
            
            return response.get('link')
            
        except Exception as e:
            self._log(f"❌ Ошибка получения ссылки для {call_id}: {e}", "ERROR")
            return None
    
    def _format_filename(self, call_data):
        # Форматирование имени файла
        # Извлекаем данные
        call_id = call_data.get('call_id', 'unknown')
        call_start = call_data.get('callstart', '')
        sip = call_data.get('sip', 'unknown')
        destination = str(call_data.get('destination', 'unknown'))
        duration = call_data.get('seconds', 0)
        
        # Разбираем дату и время
        try:
            dt = datetime.strptime(call_start, "%Y-%m-%d %H:%M:%S")
            date = dt.strftime("%Y%m%d")
            time = dt.strftime("%H%M%S")
        except:
            date = "unknown_date"
            time = "unknown_time"
        
        # Формируем имя файла
        filename = FILENAME_TEMPLATE.format(
            call_id=call_id,
            date=date,
            time=time,
            sip=sip,
            destination=destination,
            duration=duration
        )
        
        # Очищаем от недопустимых символов
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        return filename
    
    def download_file(self, url, filename):
        # Скачивание файла
        filepath = os.path.join(self.download_folder, filename)
        
        for attempt in range(MAX_DOWNLOAD_ATTEMPTS):
            try:
                self._log(f"📥 Скачиваем: {filename} (попытка {attempt + 1})")
                
                response = requests.get(url, timeout=REQUEST_TIMEOUT)
                response.raise_for_status()
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                file_size = len(response.content)
                self._log(f"✅ Сохранено: {filename} ({file_size:,} байт)")
                
                return filepath
                
            except Exception as e:
                if attempt < MAX_DOWNLOAD_ATTEMPTS - 1:
                    self._log(f"⚠️ Попытка {attempt + 1} неудачна: {e}", "WARNING")
                else:
                    self._log(f"❌ Не удалось скачать {filename}: {e}", "ERROR")
        
        return None
    
    def _print_call_info(self, call_data, index, total):
        # Вывод информации о звонке
        self._log(f"\n📞 Запись {index}/{total}:")
        self._log(f"   🆔 ID: {call_data.get('call_id')}")
        self._log(f"   ⏰ Время: {call_data.get('callstart')}")
        self._log(f"   📱 SIP: {call_data.get('sip')}")
        self._log(f"   🎯 Назначение: {call_data.get('destination')}")
        self._log(f"   ⏱️ Длительность: {call_data.get('seconds')} сек")
        self._log(f"   📊 Статус: {call_data.get('disposition')}")
    
    def download_all_records(self):
        # Основной метод для скачивания всех записей
        self._log("🎵 ZADARMA AUDIO DOWNLOADER")
        self._log("=" * 50)
        
        env = "SANDBOX" if SANDBOX_MODE else "PRODUCTION"
        self._log(f"🌍 Режим: {env}")
        self._log(f"🔑 API Key: {API_KEY[:10]}...")
        
        # Создаем папку
        self._create_download_folder()
        
        # Получаем список записей
        records = self.get_call_records()
        
        if not records:
            self._log("📭 Записи не найдены")
            return
        
        self._log(f"🎯 Начинаем скачивание {len(records)} записей...")
        
        # Скачиваем каждую запись
        for index, record in enumerate(records, 1):
            self._print_call_info(record, index, len(records))
            
            # Получаем ссылку
            download_url = self.get_download_link(record['call_id'])
            if not download_url:
                self.stats['errors'] += 1
                continue
            
            # Формируем имя файла
            filename = self._format_filename(record)
            
            # Скачиваем
            if self.download_file(download_url, filename):
                self.stats['downloaded'] += 1
            else:
                self.stats['errors'] += 1
        
        # Выводим статистику
        self._print_final_stats()
    
    def _print_final_stats(self):
        # Вывод финальной статистики
        self._log("\n" + "=" * 50)
        self._log("📊 ИТОГОВАЯ СТАТИСТИКА:")
        self._log(f"   🎵 Найдено записей: {self.stats['found']}")
        self._log(f"   ✅ Скачано успешно: {self.stats['downloaded']}")
        self._log(f"   ❌ Ошибок: {self.stats['errors']}")
        self._log(f"   📁 Папка: {self.download_folder}")
        
        if self.stats['downloaded'] > 0:
            self._log("🎉 Скачивание завершено успешно!")
        else:
            self._log("😞 Не удалось скачать файлы")


def main():
    # Главная функция
    try:
        downloader = ZadarmaDownloader()
        downloader.download_all_records()
    except KeyboardInterrupt:
        print("\n⏹️ Прервано пользователем")
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
