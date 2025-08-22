#!/usr/bin/python3
# 🔧 ZADARMA API CLIENT - ИСПРАВЛЕННАЯ ВЕРСИЯ
# ============================================
#
# 🚨 ВНИМАНИЕ: Этот код содержит критически важные исправления!
#
# РЕШЕННАЯ ПРОБЛЕМА:
# - Изначально получали ошибку: ModuleNotFoundError: No module named 'zadarma'
# - После создания модуля получали: 401 Unauthorized 
#
# КОРЕНЬ ПРОБЛЕМЫ:
# - Неправильный алгоритм генерации подписи для авторизации
# - Наша версия: base64.encode(hmac.digest()) - Base64 от сырых байтов ❌
# - Правильная: base64.encode(hmac.hexdigest().encode()) - Base64 от HEX-строки ✅
#
# ИСТОЧНИК РЕШЕНИЯ:
# - Официальная Python библиотека: https://github.com/zadarma/user-api-py-v1
# - Файл: zadarma/api.py, строки 105-111
#
# ⚠️  НЕ ИЗМЕНЯТЬ алгоритм _generate_signature без крайней необходимости!
# ⚠️  Любые изменения в авторизации могут сломать всю интеграцию!
import hashlib
import hmac
import requests
import json
import base64
from urllib.parse import urlencode


class ZadarmaAPI:
    def __init__(self, key, secret, sandbox=False):
        # Initialize Zadarma API client
        # 
        # Args:
        #     key (str): API key
        #     secret (str): API secret
        #     sandbox (bool): Use sandbox mode
        self.key = key
        self.secret = secret
        self.base_url = "https://api.zadarma.com" if not sandbox else "https://api-sandbox.zadarma.com"
    
    def _generate_signature(self, method, params=None):
        # Generate signature for API request according to Zadarma documentation
        # 
        # 🚨 КРИТИЧЕСКИ ВАЖНО: НЕ ИЗМЕНЯТЬ ЭТОТ АЛГОРИТМ!
        # Этот код был исправлен после изучения официальной библиотеки Zadarma.
        # Ключевое отличие: Base64 применяется к HEX-строке HMAC, а не к сырым байтам!
        # 
        # Источник решения: https://github.com/zadarma/user-api-py-v1
        # 
        # Args:
        #     method (str): API endpoint path
        #     params (dict): Request parameters
        #     
        # Returns:
        #     str: Generated signature
        if params is None:
            params = {}
        
        # 1. Sort parameters alphabetically (ksort in PHP)
        sorted_params = sorted(params.items())
        
        # 2. Create query string (http_build_query in PHP with RFC1738)
        from urllib.parse import urlencode
        params_string = urlencode(sorted_params) if sorted_params else ""
        
        # 3. MD5 hash of parameters string
        md5_params = hashlib.md5(params_string.encode('utf-8')).hexdigest()
        
        # 4. Create string to sign: method + params_string + md5(params_string)
        string_to_sign = f"{method}{params_string}{md5_params}"
        
        # 5. HMAC-SHA1 with secret key
        hmac_result = hmac.new(
            self.secret.encode('utf-8'), 
            string_to_sign.encode('utf-8'), 
            hashlib.sha1
        )
        
        # 6. 🚨 КРИТИЧЕСКИ ВАЖНО: Base64 encode the HEX digest (not the raw bytes!)
        # ⚠️  НЕ МЕНЯТЬ: .hexdigest() вместо .digest() - это ключевое отличие!
        # ⚠️  Официальная библиотека Zadarma делает именно так:
        # ⚠️  base64.b64encode(bytes(hmac_h.hexdigest(), 'utf8'))
        signature = base64.b64encode(
            hmac_result.hexdigest().encode('utf-8')
        ).decode('utf-8')
        
        return signature
    
    def call(self, path, params=None, method="GET"):
        # Make API call to Zadarma
        # 
        # Args:
        #     path (str): API endpoint path
        #     params (dict): Request parameters
        #     method (str): HTTP method
        #     
        # Returns:
        #     dict: API response
        if params is None:
            params = {}
        
        # Add format parameter as per official implementation
        params['format'] = 'json'
        
        # Generate signature
        signature = self._generate_signature(path, params)
        
        # Prepare headers
        headers = {
            'Authorization': f"{self.key}:{signature}"
        }
        

        # Make request
        url = f"{self.base_url}{path}"
        
        try:
            if method.upper() == "GET":
                # For GET requests, build the URL manually to match the signature
                filtered_params = {k: v for k, v in params.items() if not hasattr(v, '__dict__')}
                sorted_params = sorted(filtered_params.items())
                def rfc1738_encode(s):
                    from urllib.parse import quote
                    return quote(str(s), safe='')
                query_string = '&'.join([f"{rfc1738_encode(k)}={rfc1738_encode(v)}" for k, v in sorted_params])
                full_url = f"{url}?{query_string}"
                response = requests.get(full_url, headers=headers)
            elif method.upper() == "POST":
                # For POST requests, use form-encoded data
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
                response = requests.post(url, data=params, headers=headers)
            elif method.upper() == "PUT":
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
                response = requests.put(url, data=params, headers=headers)
            elif method.upper() == "DELETE":
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
                response = requests.delete(url, data=params, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            

            response.raise_for_status()
            return response.text
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {e}")
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse API response: {e}")
