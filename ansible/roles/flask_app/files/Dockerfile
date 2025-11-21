# --- roles/flask_app/files/Dockerfile ---
# ========================================
# FLASK APPLICATION DOCKERFILE
# ========================================
FROM python:3.11-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Копируем зависимости отдельно (для кэширования слоёв)
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY app.py .

# Порт приложения
EXPOSE 5000

# Команда запуска
CMD ["python", "app.py"]
