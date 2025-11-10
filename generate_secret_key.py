#!/usr/bin/env python
"""
Утилита для генерации нового SECRET_KEY для Django проекта
Использование: python generate_secret_key.py
"""

from django.core.management.utils import get_random_secret_key

if __name__ == '__main__':
    secret_key = get_random_secret_key()
    print("\n" + "="*60)
    print("Новый SECRET_KEY сгенерирован:")
    print("="*60)
    print(secret_key)
    print("="*60)
    print("\nСкопируйте этот ключ в файл .env:")
    print(f"SECRET_KEY={secret_key}\n")

