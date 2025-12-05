# Makefile

# Переменные
IMAGE_NAME = vershininaolga/pizzabot
BOT_CONTAINER = pizza-bot
DB_CONTAINER = pizza-db
NETWORK = pizza-net
VOLUME = pizza-db-data

.PHONY: build push network volume db-up db-down bot-up bot-down

# Сборка образа бота
build:
  docker build -t $(IMAGE_NAME) .

# Публикация образа в Docker Hub
push: build
  docker push $(IMAGE_NAME)

# Создание Docker-сети
network:
  docker network create $(NETWORK) 2>/dev/null  true

# Создание тома для БД
volume:
  docker volume create $(VOLUME)

# Запуск PostgreSQL
db-up: volume network
  docker run -d \
    --name $(DB_CONTAINER) \
    --network $(NETWORK) \
    -e POSTGRES_DB=pizza_bot \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=postgres \
    -p 5432:5432 \
    -v $(VOLUME):/var/lib/postgresql/data \
    postgres:16

# Остановка PostgreSQL
db-down:
  docker stop $(DB_CONTAINER) 2>/dev/null  true
  docker rm $(DB_CONTAINER) 2>/dev/null  true

# Запуск бота
bot-up: build db-up
  docker run -d \
    --name $(BOT_CONTAINER) \
    --network $(NETWORK) \
    -e BOT_TOKEN=$(BOT_TOKEN) \
    -e DB_HOST=$(DB_CONTAINER) \
    -e DB_PORT=5432 \
    -e DB_USER=postgres \
    -e DB_PASSWORD=postgres \
    -e DB_NAME=pizza_bot \
    $(IMAGE_NAME)

# Остановка бота
bot-down:
  docker stop $(BOT_CONTAINER) 2>/dev/null  true
  docker rm $(BOT_CONTAINER) 2>/dev/null || true