# Order API

<div align="center">

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-%23092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-%230db7ed?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
</div>

**Выполнено в рамках [тестового задания](https://app.affine.pro/workspace/250b4b65-457d-47fa-97cc-def98b124735/it0qZqZ0R57zFfJa7xVC6?mode=page)**

## Установка и запуск:

### 1. Клонирование репозитория:
```sh
git clone https://github.com/pavlowave/django_eff_Mob
cd django_eff_Mob
```

### 2. Создание .env файла:
Создайте файл `.env` в корне проекта с таким содержанием:

```bash
SECRET_KEY='django-insecure-*4c6m+yt*wts9-*)%(5*&w!c-8h^(w_@nipbo#ivxypzd9!%*d'
DEBUG=True
DB_HOST=db
DB_NAME=dbname
DB_USER=dbuser
DB_PASSWORD=pass
```

### 3. Сборка и запуск контейнеров
```bash
docker-compose up --build
```

### 4. Миграции базы данных
После запуска контейнера выполните миграции для настройки базы данных:
```sh
docker-compose exec web-app python manage.py migrate
```

### 5. Запуск тестов

```sh
docker-compose exec web-app python manage.py test modules.orders.tests.test_all
```

### 6. Доступ к приложению
Приложение будет доступно по адресу: [http://127.0.0.1:8000/api/orders/](http://127.0.0.1:8000/api/orders/)

## Использование

### Доступные представления

#### 1. Создание заказа
- **URL**: `/orders/create/`
- **Метод**: `POST`, `GET`
- **Шаблон**: `orders/create_order.html`
- **Форма**: `OrderForm`
- **Описание**: Позволяет создать новый заказ.

#### 2. Удаление заказа
- **URL**: `/orders/delete/<order_id>/`
- **Метод**: `POST`
- **Описание**: Удаляет заказ по его идентификатору.

#### 3. Обновление статуса заказа
- **URL**: `/orders/update_status/<order_id>/`
- **Метод**: `POST`
- **Шаблон**: `orders/update_order_status.html`
- **Описание**: Позволяет обновить статус заказа.

#### 4. Поиск заказов
- **URL**: `/orders/search/`
- **Метод**: `GET`
- **Шаблон**: `orders/search_orders.html`
- **Форма**: `OrderSearchForm`
- **Описание**: Позволяет искать заказы по номеру стола или статусу.

#### 5. Список заказов
- **URL**: `/orders/`
- **Метод**: `GET`
- **Шаблон**: `orders/order_list.html`
- **Форма**: `OrderSearchForm`
- **Описание**: Отображает список заказов с возможностью фильтрации.

#### 6. Расчет выручки
- **URL**: `/orders/revenue/`
- **Метод**: `GET`
- **Шаблон**: `orders/calculate_revenue.html`
- **Описание**: Рассчитывает сумму выручки от всех оплаченных заказов.

#### 7. Редактирование заказа
- **URL**: `/orders/edit/<order_id>/`
- **Метод**: `GET`, `POST`
- **Шаблон**: `orders/edit_order.html`
- **Форма**: `OrderForm`
- **Описание**: Позволяет редактировать заказ по его идентификатору.

