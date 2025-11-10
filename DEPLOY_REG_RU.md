# Инструкция по деплою на REG.RU

Подробная пошаговая инструкция для развертывания Django проекта Aidaen на VPS/облачном сервере REG.RU.

## Подготовка

### 1. Регистрация и создание сервера на REG.RU

1. Зайдите на [reg.ru](https://www.reg.ru)
2. Зарегистрируйтесь или войдите в аккаунт
3. Перейдите в раздел "VPS" или "Облачные серверы"
4. Создайте новый сервер:
   - **ОС**: Ubuntu 22.04 LTS (рекомендуется)
   - **Конфигурация**: минимум 1 CPU, 1GB RAM, 10GB SSD
   - **Регион**: выберите ближайший к вашей аудитории
5. Дождитесь создания сервера (обычно 5-10 минут)

### 2. Получение доступа к серверу

После создания сервера REG.RU предоставит:
- **IP-адрес сервера**
- **Логин** (обычно `root`)
- **Пароль** (или SSH ключ)

Сохраните эти данные в безопасном месте!

## Подключение к серверу

### Windows

Используйте PuTTY или Windows Terminal:

```bash
ssh root@ваш-ip-адрес
```

### Linux/Mac

```bash
ssh root@ваш-ip-адрес
```

При первом подключении подтвердите добавление сервера в известные хосты.

## Деплой проекта

### Вариант 1: Автоматический деплой (рекомендуется)

1. Загрузите проект на сервер через Git или SCP:

```bash
# Через Git (если проект в репозитории)
cd /var/www
git clone https://github.com/ваш-username/ваш-репозиторий.git SITE_PROEKT
cd SITE_PROEKT

# Или через SCP с вашего компьютера:
# scp -r C:\Games\SITE_PROEKT root@ваш-ip:/var/www/
```

2. Запустите скрипт автоматизации:

```bash
cd /var/www/SITE_PROEKT
chmod +x deploy.sh
sudo bash deploy.sh
```

Скрипт автоматически:
- Установит все зависимости
- Настроит PostgreSQL
- Создаст базу данных
- Настроит Gunicorn и Nginx
- Применит миграции
- Соберет статические файлы

**В процессе выполнения скрипт попросит ввести:**
- Имя базы данных (по умолчанию: `aidaen_db`)
- Имя пользователя БД (по умолчанию: `aidaen_user`)
- Пароль для пользователя БД
- Домен или IP для ALLOWED_HOSTS
- Данные для суперпользователя Django

### Вариант 2: Ручной деплой

Если предпочитаете ручную настройку, следуйте инструкциям ниже.

#### Шаг 1: Обновление системы

```bash
apt update
apt upgrade -y
```

#### Шаг 2: Установка системных пакетов

```bash
apt install -y python3 python3-pip python3-venv python3-dev \
    postgresql postgresql-contrib \
    nginx \
    git \
    build-essential \
    libpq-dev \
    curl
```

#### Шаг 3: Настройка PostgreSQL

```bash
# Запуск PostgreSQL
systemctl start postgresql
systemctl enable postgresql

# Подключение к PostgreSQL
sudo -u postgres psql
```

В консоли PostgreSQL выполните:

```sql
CREATE DATABASE aidaen_db;
CREATE USER aidaen_user WITH PASSWORD 'ваш-надежный-пароль';
GRANT ALL PRIVILEGES ON DATABASE aidaen_db TO aidaen_user;
\q
```

#### Шаг 4: Развертывание проекта

```bash
# Переход в директорию для проектов
cd /var/www

# Клонирование или копирование проекта
git clone ваш-репозиторий SITE_PROEKT
# или
# scp -r путь/к/проекту root@ваш-ip:/var/www/SITE_PROEKT

cd SITE_PROEKT
```

#### Шаг 5: Создание виртуального окружения

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

#### Шаг 6: Настройка переменных окружения

```bash
# Копирование примера
cp env.example .env

# Редактирование .env
nano .env
```

Заполните файл `.env`:

```env
SECRET_KEY=сгенерируйте-новый-ключ
DEBUG=False
ALLOWED_HOSTS=ваш-домен.ru,www.ваш-домен.ru,ваш-ip-адрес

DB_NAME=aidaen_db
DB_USER=aidaen_user
DB_PASSWORD=ваш-пароль-из-шага-3
DB_HOST=localhost
DB_PORT=5432
```

Для генерации SECRET_KEY:

```bash
python generate_secret_key.py
```

#### Шаг 7: Применение миграций

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

#### Шаг 8: Настройка Gunicorn

```bash
# Копирование примера конфигурации
sudo cp gunicorn.service.example /etc/systemd/system/gunicorn.service

# Редактирование конфигурации
sudo nano /etc/systemd/system/gunicorn.service
```

Обновите пути в файле:
- `WorkingDirectory=/var/www/SITE_PROEKT`
- `ExecStart=/var/www/SITE_PROEKT/venv/bin/gunicorn ...`

Запуск сервиса:

```bash
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn
```

#### Шаг 9: Настройка Nginx

```bash
# Копирование примера конфигурации
sudo cp nginx.conf.example /etc/nginx/sites-available/aidaen

# Редактирование конфигурации
sudo nano /etc/nginx/sites-available/aidaen
```

Обновите:
- Пути к статическим и медиа файлам
- Домен в `server_name`

Создание символической ссылки:

```bash
sudo ln -s /etc/nginx/sites-available/aidaen /etc/nginx/sites-enabled/
```

Проверка и перезагрузка:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

## Настройка домена (опционально)

Если у вас есть домен, зарегистрированный на REG.RU:

1. Зайдите в панель управления доменами REG.RU
2. Найдите ваш домен и откройте настройки DNS
3. Добавьте A-запись:
   - **Имя**: `@` (или `www` для поддомена)
   - **Тип**: A
   - **Значение**: IP-адрес вашего сервера
   - **TTL**: 3600

4. Обновите `.env` файл:
   ```env
   ALLOWED_HOSTS=ваш-домен.ru,www.ваш-домен.ru
   ```

5. Обновите конфигурацию Nginx с вашим доменом

## Настройка SSL (HTTPS)

Для безопасности обязательно настройте SSL сертификат:

```bash
# Установка Certbot
apt install -y certbot python3-certbot-nginx

# Получение сертификата
sudo certbot --nginx -d ваш-домен.ru -d www.ваш-домен.ru

# Автоматическое обновление
sudo certbot renew --dry-run
```

После получения сертификата обновите `.env`:

```env
SECURE_SSL_REDIRECT=True
```

И перезапустите Gunicorn:

```bash
sudo systemctl restart gunicorn
```

## Проверка работы

1. Откройте браузер и перейдите по адресу вашего сервера
2. Проверьте админ-панель: `http://ваш-домен.ru/admin/`
3. Проверьте создание новостей

## Управление проектом

### Просмотр логов

```bash
# Логи Gunicorn
sudo journalctl -u gunicorn -f

# Логи Nginx
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# Логи Django (если настроены)
tail -f /var/www/SITE_PROEKT/logs/django.log
```

### Перезапуск сервисов

```bash
# Перезапуск Gunicorn
sudo systemctl restart gunicorn

# Перезапуск Nginx
sudo systemctl restart nginx

# Перезапуск PostgreSQL
sudo systemctl restart postgresql
```

### Обновление проекта

```bash
cd /var/www/SITE_PROEKT
source venv/bin/activate

# Обновление кода (если через Git)
git pull

# Обновление зависимостей
pip install -r requirements.txt

# Применение новых миграций
python manage.py migrate

# Сбор статических файлов
python manage.py collectstatic --noinput

# Перезапуск Gunicorn
sudo systemctl restart gunicorn
```

## Troubleshooting

### Ошибка: "502 Bad Gateway"

Проверьте статус Gunicorn:

```bash
sudo systemctl status gunicorn
```

Если сервис не запущен, проверьте логи:

```bash
sudo journalctl -u gunicorn -n 50
```

### Ошибка подключения к базе данных

Проверьте настройки в `.env` и убедитесь, что PostgreSQL запущен:

```bash
sudo systemctl status postgresql
sudo -u postgres psql -l
```

### Статические файлы не загружаются

Убедитесь, что выполнили:

```bash
python manage.py collectstatic --noinput
```

Проверьте права на директорию:

```bash
sudo chown -R www-data:www-data /var/www/SITE_PROEKT/staticfiles
```

### Ошибка "DisallowedHost"

Проверьте `ALLOWED_HOSTS` в `.env` и убедитесь, что домен/IP указан правильно.

### Проблемы с правами доступа

```bash
sudo chown -R www-data:www-data /var/www/SITE_PROEKT
sudo chmod -R 755 /var/www/SITE_PROEKT
sudo chmod 600 /var/www/SITE_PROEKT/.env
```

## Безопасность

1. **Настройте файрвол:**
   ```bash
   sudo ufw allow 22/tcp
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```

2. **Измените пароль root:**
   ```bash
   passwd
   ```

3. **Создайте отдельного пользователя (рекомендуется):**
   ```bash
   adduser deploy
   usermod -aG sudo deploy
   ```

4. **Настройте SSH ключи** вместо паролей

5. **Регулярно обновляйте систему:**
   ```bash
   apt update && apt upgrade -y
   ```

## Поддержка

При возникновении проблем:
1. Проверьте логи сервисов
2. Убедитесь, что все переменные окружения установлены правильно
3. Проверьте конфигурации Nginx и Gunicorn
4. Обратитесь в поддержку REG.RU при проблемах с сервером

## Полезные команды

```bash
# Проверка использования диска
df -h

# Проверка использования памяти
free -h

# Проверка запущенных процессов
ps aux | grep gunicorn

# Проверка портов
netstat -tulpn | grep :80
netstat -tulpn | grep :8000
```

