# Базовий образ — легкий Python 3.12
FROM python:3.12-slim

# Робоча директорія всередині контейнера
WORKDIR /app

# Спочатку копіюємо лише requirements.txt — так Docker кешує шар
# з залежностями і не перевстановлює їх при кожній зміні коду.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Тепер копіюємо сам код
COPY demo_app.py .

# Директорія для логів, яку будемо монтувати як volume з хоста
RUN mkdir -p /app/logs

# Команда запуску контейнера
CMD ["python", "demo_app.py"]
