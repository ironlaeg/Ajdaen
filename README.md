# Aidaen - Национальная газета Осетии

Современный новостной сайт с красивым дизайном в цветах флага Осетии.

## Особенности

### 🎨 Дизайн
- **Цветовая схема**: Основана на цветах флага Осетии (белый, красный, желтый) с зелеными оттенками
- **Современный интерфейс**: Корпоративный стиль с анимациями и интерактивными элементами
- **Адаптивность**: Оптимизирован для десктопных устройств
- **Типографика**: Google Fonts (Playfair Display, Roboto)

### 🚀 Функциональность
- **Изображения к новостям**: Поддержка загрузки и отображения изображений
- **Категории и теги**: Организация контента с фильтрацией
- **Поиск**: Полнотекстовый поиск по заголовкам и содержанию
- **Архив**: Организация новостей по месяцам и годам
- **Черновики**: Система черновиков для авторов
- **Социальные кнопки**: Поделиться в социальных сетях

### 🛠 Технологии
- **Backend**: Django 5.2
- **Frontend**: Bootstrap 5.3, Font Awesome 6, AOS (Animate On Scroll)
- **JavaScript**: Vanilla JS с интерактивными элементами
- **CSS**: Кастомные стили с CSS переменными и анимациями

## Установка и запуск

### Требования
- Python 3.8+
- Django 5.2+
- PostgreSQL (для продакшна)

### Установка для разработки
1. Клонируйте репозиторий
2. Создайте виртуальное окружение:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate  # Windows
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Создайте файл `.env` на основе `env.example`:
   ```bash
   cp env.example .env
   ```
   Отредактируйте `.env` и установите `DEBUG=True` для разработки.

5. Примените миграции:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Создайте суперпользователя:
   ```bash
   python manage.py createsuperuser
   ```

7. Соберите статические файлы:
   ```bash
   python manage.py collectstatic --noinput
   ```

8. Запустите сервер:
   ```bash
   python manage.py runserver
   ```

### Настройка медиа-файлов
В `settings.py` уже настроены:
- `MEDIA_URL = '/media/'`
- `MEDIA_ROOT = BASE_DIR / 'media'`

В `urls.py` добавлена обработка медиа-файлов в режиме разработки.

## Структура проекта

```
Aidaen/
├── static/
│   ├── css/
│   │   └── style.css          # Основные стили
│   ├── js/
│   │   └── main.js            # JavaScript функциональность
│   └── images/                # Статические изображения
├── media/
│   └── news_images/           # Загруженные изображения новостей
├── templates/
│   ├── base.html              # Базовый шаблон
│   ├── headline_list.html     # Список новостей
│   ├── headline_detail.html   # Детальная страница новости
│   ├── headline_form.html     # Форма создания/редактирования
│   ├── headline_confirm_delete.html
│   ├── headline_draft_list.html
│   ├── headline_archive.html
│   └── headline_month.html
├── news/
│   ├── models.py              # Модели данных
│   ├── views.py               # Представления
│   ├── forms.py               # Формы
│   ├── admin.py               # Админка
│   └── urls.py                # URL маршруты
└── manage.py
```

## Модели данных

### Headline (Новость)
- `title` - Заголовок
- `content` - Содержание
- `short_description` - Краткое описание
- `image` - Изображение
- `pdf_file` - PDF файл
- `tags` - Теги (ManyToMany)
- `status` - Статус (draft/published)
- `author` - Автор
- `created_at` - Дата создания
- `published_at` - Дата публикации

### Tag (Тег)
- `name` - Название
- `slug` - URL slug
- `created_at` - Дата создания

## Использование

### Создание новости
1. Войдите в систему через `/admin/`
2. Перейдите на главную страницу
3. Нажмите "Создать новость"
4. Заполните форму с изображением, PDF файлом (опционально) и тегами
5. Выберите статус "Опубликовано" или "Черновик"

### Управление тегами
- Перейдите в админку `/admin/`
- Добавьте теги для организации контента

### Фильтрация новостей
- Кликайте по тегам в блоке "Популярные теги" для просмотра связанных новостей
- Используйте поиск для поиска по тексту
- Используйте фильтры в сайдбаре справа

## Цветовая палитра

```css
:root {
    --ossetia-white: #FFFFFF;
    --ossetia-red: #C1272D;
    --ossetia-yellow: #FFD100;
    --ossetia-green-dark: #2D5016;
    --ossetia-green-medium: #4A7C59;
    --ossetia-green-light: #7BA05B;
    --ossetia-green-pale: #E8F5E8;
}
```

## Анимации и интерактивность

- **AOS (Animate On Scroll)**: Анимации при прокрутке
- **Hover эффекты**: Интерактивные элементы при наведении
- **Плавные переходы**: CSS transitions для всех элементов
- **Превью изображений**: Drag & drop загрузка с превью
- **Социальные кнопки**: Поделиться в соцсетях
- **Уведомления**: Toast уведомления для действий

## Разработка

### Добавление новых функций
1. Обновите модели в `news/models.py`
2. Создайте миграции: `python manage.py makemigrations`
3. Примените миграции: `python manage.py migrate`
4. Обновите формы, представления и шаблоны
5. Добавьте URL маршруты

### Кастомизация стилей
Основные стили находятся в `static/css/style.css`. Используйте CSS переменные для изменения цветов:

```css
:root {
    --ossetia-green-dark: #2D5016; /* Основной зеленый */
    --ossetia-red: #C1272D;        /* Красный флага */
    --ossetia-yellow: #FFD100;     /* Желтый флага */
}
```

## Деплой

### Облачные платформы (Railway, Heroku, DigitalOcean)

1. **Подготовка окружения:**
   - Скопируйте `env.example` в `.env` и заполните переменные окружения
   - Создайте PostgreSQL базу данных на платформе
   - Установите переменные окружения на платформе

2. **Переменные окружения для облачной платформы:**
   ```
   SECRET_KEY=сгенерируйте-новый-секретный-ключ
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   DB_NAME=название_базы
   DB_USER=пользователь_бд
   DB_PASSWORD=пароль_бд
   DB_HOST=хост_бд
   DB_PORT=5432
   ```

3. **Деплой на Railway:**
   - Подключите Git репозиторий
   - Railway автоматически определит `Procfile`
   - Настройте PostgreSQL базу данных в разделе Databases
   - Установите переменные окружения в разделе Variables

4. **Деплой на Heroku:**
   ```bash
   heroku create your-app-name
   heroku addons:create heroku-postgresql:hobby-dev
   heroku config:set SECRET_KEY=ваш-секретный-ключ
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
   git push heroku main
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

5. **После деплоя:**
   ```bash
   # Примените миграции
   python manage.py migrate
   
   # Соберите статические файлы
   python manage.py collectstatic --noinput
   
   # Создайте суперпользователя
   python manage.py createsuperuser
   ```

### REG.RU VPS (Рекомендуется для России)

**Подробная инструкция:** См. [DEPLOY_REG_RU.md](DEPLOY_REG_RU.md)

**Быстрый старт:**

1. **Создайте VPS на REG.RU:**
   - Зайдите на [reg.ru](https://www.reg.ru)
   - Создайте VPS с Ubuntu 22.04 LTS
   - Получите IP-адрес и доступ к серверу

2. **Подключитесь к серверу:**
   ```bash
   ssh root@ваш-ip-адрес
   ```

3. **Загрузите проект:**
   ```bash
   cd /var/www
   git clone ваш-репозиторий SITE_PROEKT
   # или через scp с вашего компьютера
   ```

4. **Запустите автоматический деплой:**
   ```bash
   cd /var/www/SITE_PROEKT
   chmod +x deploy.sh
   sudo bash deploy.sh
   ```

   Скрипт автоматически выполнит все настройки!

5. **Настройте домен и SSL:**
   - Добавьте A-запись в DNS на REG.RU
   - Установите SSL: `sudo certbot --nginx -d ваш-домен.ru`

**Для ручной настройки** см. [DEPLOY_REG_RU.md](DEPLOY_REG_RU.md)

### VPS сервер (Nginx + Gunicorn) - Общая инструкция

1. **Установка зависимостей на сервере:**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx postgresql postgresql-contrib
   ```

2. **Настройка PostgreSQL:**
   ```bash
   sudo -u postgres psql
   CREATE DATABASE your_db_name;
   CREATE USER your_db_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_db_user;
   \q
   ```

3. **Развертывание проекта:**
   ```bash
   cd /var/www/
   git clone your-repository
   cd SITE_PROEKT
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   cp env.example .env
   nano .env  # Отредактируйте переменные окружения
   ```

4. **Настройка Gunicorn:**
   ```bash
   # Скопируйте пример systemd сервиса
   sudo cp gunicorn.service.example /etc/systemd/system/gunicorn.service
   sudo nano /etc/systemd/system/gunicorn.service  # Обновите пути
   sudo systemctl daemon-reload
   sudo systemctl start gunicorn
   sudo systemctl enable gunicorn
   ```

5. **Настройка Nginx:**
   ```bash
   # Скопируйте пример конфигурации
   sudo cp nginx.conf.example /etc/nginx/sites-available/your-site
   sudo nano /etc/nginx/sites-available/your-site  # Обновите пути и домен
   sudo ln -s /etc/nginx/sites-available/your-site /etc/nginx/sites-enabled/
   sudo nginx -t  # Проверьте конфигурацию
   sudo systemctl reload nginx
   ```

6. **SSL сертификат (Let's Encrypt):**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
   ```

7. **Соберите статические файлы:**
   ```bash
   python manage.py collectstatic --noinput
   ```

### Генерация нового SECRET_KEY

Для продакшна сгенерируйте новый SECRET_KEY:

**Вариант 1: Используя скрипт (рекомендуется):**
```bash
python generate_secret_key.py
```

**Вариант 2: Через Django команду:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Безопасность

- **Никогда не коммитьте `.env` файл в Git**
- **Используйте сложный SECRET_KEY для продакшна**
- **Установите DEBUG=False в продакшн**
- **Настройте SSL/HTTPS для продакшна**
- **Используйте PostgreSQL вместо SQLite в продакшне**
- **Регулярно обновляйте зависимости**

## Лицензия

Проект создан для национальной газеты Осетии Aidaen.

## Поддержка

Для вопросов и предложений обращайтесь к разработчику.
