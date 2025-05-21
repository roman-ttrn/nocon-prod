#!/bin/sh

# ❗ Остановить скрипт, если что-то ломается
set -e

echo "⏳ Ожидаем подключения к PostgreSQL..."

# Ждём, пока PostgreSQL будет доступна
until nc -z "$DB_HOST" "$DB_PORT"; do
  echo "База данных $DB_HOST:$DB_PORT пока не доступна, ждём..."
  sleep 1
done

echo "✅ База данных доступна, продолжаем..."

# Прогоняем миграции
echo "📦 Применяем миграции..."
python manage.py migrate --noinput

# Собираем статические файлы (если используется)
echo "📁 Собираем статику..."
python manage.py collectstatic --noinput

# Можно также создать суперпользователя, если нужен (опционально)

# Запускаем Daphne
echo "🚀 Запускаем Daphne..."
daphne -b 0.0.0.0 -p 8000 nocon.asgi:application
