FROM python:3.11-slim
WORKDIR /app

# Установка системных сертификатов для TLS/SSL
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates openssl \
 && update-ca-certificates \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]