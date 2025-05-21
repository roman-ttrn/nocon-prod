#############################
# ЭТАП 1: Сборка проекта
#############################

FROM python:3.11.8-slim AS banana
# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Устанавливаем системные библиотеки, необходимые для компиляции зависимостей и работы с изображениями
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    # Компилятор для C/C++ — нужен для сборки некоторых Python-зависимостей
    libpq-dev \
    # Для PostgreSQL (psycopg2)
    libjpeg-dev \
    # Для Pillow (обработка изображений)
    zlib1g-dev \          
    # Для Pillow
    libwebp-dev \         
    # Для Pillow (WebP)
    netcat \              
    # Для healthcheck или ожидания других сервисов
    curl \                
    # Можно использовать для отладки
    && rm -rf /var/lib/apt/lists/*  
    # Очищаем кэш apt после установки

# Создаём виртуальное окружение внутри контейнера
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Копируем зависимости и устанавливаем
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем весь проект (на этом этапе ты можешь добавить .dockerignore, чтобы не тащить лишние файлы)
COPY . .

# Делаем entrypoint.sh исполняемым, без /app/, так как WORKDIR уже /app
RUN chmod +x entrypoint.sh  

#############################
# ЭТАП 2: Финальный контейнер
#############################

FROM python:3.11.8-slim

# Копируем собранное виртуальное окружение из builder
COPY --from=banana /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Устанавливаем минимальный набор библиотек, нужных в runtime (в продакшне!)
RUN apt-get update && apt-get install -y \
    libpq5 \               
    # PostgreSQL runtime
    libjpeg62-turbo \      
    # Pillow runtime (JPEG)
    zlib1g \               
    # Pillow runtime (ZIP)
    libwebp6 \             
    # Pillow runtime (WebP)
    && rm -rf /var/lib/apt/lists/*

# Назначаем рабочую директорию
WORKDIR /app

# Копируем только необходимые финальные файлы из builder
COPY --from=banana /app .

# 🎯 Удалять не надо, если у тебя media/ уже есть локально — ты можешь **смонтировать** её в docker-compose.
# Этот RUN mkdir -p /app/media безопасен — он ничего не ломает. Но можно **убрать**, если уверен, что media уже существует:
# RUN mkdir -p /app/media && chmod -R 755 /app/media

# Безопасные переменные окружения
ENV PYTHONHASHSEED=random \
    IMAGEIO_FFMPEG_EXE=/usr/bin/ffmpeg

# Команда запуска — через shell-скрипт, где можно запускать миграции, collectstatic и т.д.
CMD ["sh", "entrypoint.sh"]
