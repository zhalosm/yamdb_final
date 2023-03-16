# CI и CD проекта api_yamdb

Rest api проекта yamdb. Проект собирает отзывы пользовтелей на произведения - книги, музыка, фильмы. 
Приозведения деляться на жанры, категории и имеют рейтинг.

# Workflow

- проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8) и запуск pytest
- сборка и доставка докер-образа для контейнера web на Docker Hub
- автоматический деплой проекта на боевой сервер
- отправка уведомления в Telegram о том, что процесс деплоя успешно завершился

![example branch parameter](https://github.com/github/docs/actions/workflows/main.yml/badge.svg?branch=master)

# Стэк технологий

- Python
- Django Rest Framework
- Postgres
- Docker
- nginx

# Запуск проекта в контейнере

Клонировать репозиторий:

```
https://github.com/zhalosm/infra_sp2.git
```

Перейти в папку с файлом docker-compose.yaml:

```
cd infra
```

Собираем контйенеры и запускаем их:

```
docker-compose up -d --build
```

Выполняем миграцию:

```
docker-compose exec web python manage.py migrate
```

Создаем суперпользователя:

```
docker-compose exec web python manage.py createsuperuser
```

Собираем статику:

```
docker-compose exec web python manage.py collectstatic --no-input
```

Cоздание дамп (резервной копии) базы:

```
docker-compose exec web python manage.py dumpdata > fixtures.json
```

Остновка и удаление контйенров.

```
docker-compose down -v
```

# Шалблон наполнения env-файла:

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
# Запуск проекта на удаленном сервере

Остановите службу nginx

```
sudo systemctl stop nginx
```

Установите Docker 

```
sudo apt install docker.io
```

Установите Docker-compose https://docs.docker.com/compose/install/

Скопируйте файлы docker-compose.yaml и nginx/default.conf из вашего проекта на сервер в 
home/<ваш_username>/docker-compose.yaml и home/<ваш_username>/nginx/default.conf соответственно.

```
scp docker-compose.yaml <username>@<host>/home/<username>/docker-compose.yaml
sudo mkdir nginx
scp default.conf <username>@<host>/home/<username>/nginx/default.conf
```

Добавьте в Secrets GitHub Actions данные:

```
DOCKER_USERNAME = имя пользователя в DockerHub
DOCKER_PASSWORD = пароль пользователя в DockerHub
HOST = ip-адрес сервера
USER = пользователь
SSH_KEY = приватный ключ с компьютера, имеющего доступ к серверу
PASSPHRASE = пароль для ssh-ключа
DB_ENGINE = django.db.backends.postgresql
DB_HOST = db
DB_PORT = 5432
DB_NAME = postgres 
POSTGRES_USER = postgres 
POSTGRES_PASSWORD = postgres
TELEGRAM_TO = id своего телеграм-аккаунта
TELEGRAM_TOKEN = токен бота
```

# После успешного деплоя

Выполняем миграцию:

```
sudo docker-compose exec web python manage.py migrate
```

Создаем суперпользователя:

```
sudo docker-compose exec web python manage.py createsuperuser
```

Собираем статику:

```
sudo docker-compose exec web python manage.py collectstatic --no-input
```

# Примеры запросов к API

Получение списка всех произведений

```
GET http://localhost/api/v1/titles/
```

Добавить новое произведение.
Права доступа: Администратор.

```
POST http://localhost/api/v1/titles/
```

Параметры json
```
{
"name": "string",
"year": 0,
"description": "string",
"genre": [
"string"
],
"category": "string"
}
```

Документация доступна по эндпойнту: http://localhost/redoc/

Авторы проекта:

Петров Константин, Виталий Коломойцев
