
<h1 align="center">Django + Docker + PostgreSQL Template</h1>

<div align="center">

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-%23092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-%230db7ed?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
</div>

Выполнено в рамках [тестового задания](https://app.affine.pro/workspace/250b4b65-457d-47fa-97cc-def98b124735/it0qZqZ0R57zFfJa7xVC6?mode=page)

## Установка и запуск:

1. Клонирование репозитория:

```
git clone https://github.com/pavlowave/django_eff_Mob
cd django_eff_Mob
```

2. Создание .env файла:
Создайте файл .env в корне проекта с таким содержанием:

```bash
SECRET_KEY='django-insecure-*4c6m+yt*wts9-*)%(5*&w!c-8h^(w_@nipbo#ivxypzd9!%*d'
DEBUG=True
DB_HOST=db
DB_NAME=dbname
DB_USER=dbuser
DB_PASSWORD=pass
```

3. Сборка и запуск контейнеров
```bash
docker-compose up --build
```

4. Миграции базы данных После запуска контейнера выполните миграции для настройки базы данных:
```
docker-compose exec web-app python manage.py migrate
```
5. Приложение будет доступно по адресу: [http://127.0.0.1:8000/](http://127.0.0.1:8000/api/orders/)

## Структура проекта

* **Dockerfile**: Конфигурация для сборки образа Docker.
* **docker-compose.yml**: Описание сервисов (Django и PostgreSQL).
* **requirements.txt**: Список Python-зависимостей.
* **.env**: Конфиденциальные настройки (игнорируется в Git).
* **settings.py**: Подключение переменных окружения для конфигурации Django.

## Как использовать

Этот шаблон подходит для:

* Создания новых Django проектов.
* Изучения работы с Docker для Django приложений.
* Быстрого прототипирования веб-приложений.

## Заметки

* Убедитесь, что Docker и Docker Compose установлены на вашей машине.
