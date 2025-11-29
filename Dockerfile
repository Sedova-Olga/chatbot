FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ждём готовности БД
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

CMD ["sh", "-c", "until pg_isready -h $DB_HOST -p $DB_PORT; do sleep 1; done && python main.py"]