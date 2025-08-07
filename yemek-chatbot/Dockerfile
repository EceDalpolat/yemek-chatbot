FROM python:3.9-slim

WORKDIR /app

# Sistem paketlerini yükle
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodlarını kopyala
COPY . .

# Port expose et
EXPOSE 8000

# Uygulamayı başlat
CMD ["uvicorn", "src.chatbot.api:app", "--host", "0.0.0.0", "--port", "8000"]