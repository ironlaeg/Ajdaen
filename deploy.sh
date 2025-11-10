#!/bin/bash

# Скрипт автоматизации деплоя Django проекта на REG.RU VPS
# Использование: sudo bash deploy.sh

set -e  # Остановка при ошибке

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Функция для вывода сообщений
info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Проверка прав root
if [ "$EUID" -ne 0 ]; then 
    error "Пожалуйста, запустите скрипт с правами root (sudo bash deploy.sh)"
    exit 1
fi

info "Начинаем деплой Django проекта на REG.RU..."

# Получаем путь к проекту
PROJECT_DIR=$(pwd)
if [ ! -f "$PROJECT_DIR/manage.py" ]; then
    error "manage.py не найден. Убедитесь, что вы находитесь в корне проекта."
    exit 1
fi

info "Проект найден в: $PROJECT_DIR"

# Обновление системы
info "Обновление системы..."
apt update
apt upgrade -y

# Установка системных пакетов
info "Установка системных пакетов..."
apt install -y python3 python3-pip python3-venv python3-dev \
    postgresql postgresql-contrib \
    nginx \
    git \
    build-essential \
    libpq-dev \
    curl

# Проверка установки PostgreSQL
info "Проверка PostgreSQL..."
systemctl start postgresql
systemctl enable postgresql

# Создание виртуального окружения
info "Создание виртуального окружения..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    info "Виртуальное окружение создано"
else
    warn "Виртуальное окружение уже существует"
fi

# Активация виртуального окружения и установка зависимостей
info "Установка зависимостей Python..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Настройка PostgreSQL
info "Настройка PostgreSQL..."
read -p "Введите имя базы данных (по умолчанию: aidaen_db): " DB_NAME
DB_NAME=${DB_NAME:-aidaen_db}

read -p "Введите имя пользователя БД (по умолчанию: aidaen_user): " DB_USER
DB_USER=${DB_USER:-aidaen_user}

read -sp "Введите пароль для пользователя БД: " DB_PASSWORD
echo ""

# Создание базы данных и пользователя
info "Создание базы данных и пользователя PostgreSQL..."
sudo -u postgres psql <<EOF
-- Создание пользователя
CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';

-- Создание базы данных
CREATE DATABASE $DB_NAME OWNER $DB_USER;

-- Предоставление прав
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;

-- Выход
\q
EOF

info "База данных $DB_NAME и пользователь $DB_USER созданы"

# Настройка .env файла
info "Настройка переменных окружения..."
if [ ! -f ".env" ]; then
    if [ -f "env.example" ]; then
        cp env.example .env
        info "Файл .env создан из env.example"
    else
        error "Файл env.example не найден!"
        exit 1
    fi
fi

# Генерация SECRET_KEY
info "Генерация SECRET_KEY..."
SECRET_KEY=$(python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")

# Обновление .env файла
sed -i "s|SECRET_KEY=.*|SECRET_KEY=$SECRET_KEY|" .env
sed -i "s|DEBUG=.*|DEBUG=False|" .env
sed -i "s|DB_NAME=.*|DB_NAME=$DB_NAME|" .env
sed -i "s|DB_USER=.*|DB_USER=$DB_USER|" .env
sed -i "s|DB_PASSWORD=.*|DB_PASSWORD=$DB_PASSWORD|" .env
sed -i "s|DB_HOST=.*|DB_HOST=localhost|" .env
sed -i "s|DB_PORT=.*|DB_PORT=5432|" .env

read -p "Введите домен или IP для ALLOWED_HOSTS (через запятую, например: example.com,www.example.com): " ALLOWED_HOSTS
if [ ! -z "$ALLOWED_HOSTS" ]; then
    sed -i "s|ALLOWED_HOSTS=.*|ALLOWED_HOSTS=$ALLOWED_HOSTS|" .env
fi

info "Файл .env настроен"

# Применение миграций
info "Применение миграций базы данных..."
python manage.py migrate

# Сбор статических файлов
info "Сбор статических файлов..."
python manage.py collectstatic --noinput

# Создание суперпользователя
info "Создание суперпользователя Django..."
warn "Вам нужно будет ввести данные для суперпользователя"
python manage.py createsuperuser

# Настройка прав на файлы
info "Настройка прав на файлы..."
chown -R www-data:www-data "$PROJECT_DIR"
chmod -R 755 "$PROJECT_DIR"
chmod 600 .env

# Настройка Gunicorn systemd сервиса
info "Настройка Gunicorn systemd сервиса..."
if [ -f "gunicorn.service.example" ]; then
    GUNICORN_SERVICE="/etc/systemd/system/gunicorn.service"
    
    # Замена путей в примере
    sed "s|/path/to/your/project/SITE_PROEKT|$PROJECT_DIR|g; s|/path/to/venv|$PROJECT_DIR/venv|g" \
        gunicorn.service.example > /tmp/gunicorn.service
    
    cp /tmp/gunicorn.service "$GUNICORN_SERVICE"
    
    systemctl daemon-reload
    systemctl enable gunicorn
    systemctl start gunicorn
    
    info "Gunicorn сервис настроен и запущен"
else
    warn "Файл gunicorn.service.example не найден, пропускаем настройку Gunicorn"
fi

# Настройка Nginx
info "Настройка Nginx..."
if [ -f "nginx.conf.example" ]; then
    read -p "Введите имя домена для Nginx конфигурации (по умолчанию: aidaen): " SITE_NAME
    SITE_NAME=${SITE_NAME:-aidaen}
    
    NGINX_SITE="/etc/nginx/sites-available/$SITE_NAME"
    
    # Замена путей и домена в примере
    sed "s|/path/to/your/project/SITE_PROEKT|$PROJECT_DIR|g; s|yourdomain.com|$ALLOWED_HOSTS|g; s|www.yourdomain.com|www.$ALLOWED_HOSTS|g" \
        nginx.conf.example > /tmp/nginx.conf
    
    cp /tmp/nginx.conf "$NGINX_SITE"
    
    # Создание символической ссылки
    if [ ! -L "/etc/nginx/sites-enabled/$SITE_NAME" ]; then
        ln -s "$NGINX_SITE" "/etc/nginx/sites-enabled/$SITE_NAME"
    fi
    
    # Проверка конфигурации Nginx
    if nginx -t; then
        systemctl reload nginx
        info "Nginx настроен и перезагружен"
    else
        error "Ошибка в конфигурации Nginx!"
        exit 1
    fi
else
    warn "Файл nginx.conf.example не найден, пропускаем настройку Nginx"
fi

# Проверка статуса сервисов
info "Проверка статуса сервисов..."
systemctl status gunicorn --no-pager || warn "Gunicorn не запущен"
systemctl status nginx --no-pager || warn "Nginx не запущен"

info "Деплой завершен!"
info "Проект доступен по адресу: http://$ALLOWED_HOSTS"
warn "Не забудьте настроить SSL сертификат (Let's Encrypt) для HTTPS"
info "Для настройки SSL выполните: sudo certbot --nginx -d $ALLOWED_HOSTS"

