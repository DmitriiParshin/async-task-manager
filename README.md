# Асинхронная система управления задачами

Этот проект представляет собой Django-приложение с использованием Django REST Framework (DRF) и Celery для управления задачами. Приложение позволяет пользователям создавать задачи через API, отслеживать их статус и получать результат выполнения. Авторизация реализована с использованием JWT.

---

## Функционал

1. **Регистрация и авторизация пользователей через API:**
   - Регистрация: `/api/register/`
   - Получение JWT-токена: `/api/token/`
   - Обновление JWT-токена: `/api/token/refresh/`

2. **Управление задачами:**
   - Создание задачи: `/api/tasks/create/`
   - Получение списка задач с фильтрацией и пагинацией: `/api/tasks/`
   - Просмотр статуса и результата конкретной задачи: `/api/tasks/<task_id>/`

3. **Типы задач:**
   - **Суммирование чисел:** Выполняет сложение чисел, указанных в массиве `numbers`.
   - **Обратный отсчёт:** Ожидает указанное количество секунд, затем возвращает сообщение о завершении.

4. **Ограничения:**
   - Пользователь может иметь одновременно не более 5 активных задач (в статусах `Запланировано` или `Выполняется`).

---

## Используемые технологии

- **Python 3.9+**
- **Django**
- **Django REST Framework**
- **Celery** для асинхронной обработки задач
- **Redis** в качестве брокера для Celery
- **djangorestframework-simplejwt** для JWT-авторизации

---

## Установка и запуск

### 1. Клонирование репозитория

Склонируйте репозиторий на вашу локальную машину:

```
git clone https://github.com/DmitriiParshin/async-task-manager.git
cd async-task-manager
```

### 2. Запуск проекта

Запустите проект:

```
docker compose up -d --build
```

## Проверка запросов в Postman

### Файл `PostmanCollection.json` - это коллекция для импорта в Postman

## Использование API

### Регистрация пользователя

- **URL:** `POST /api/register/`  
- **Пример запроса:**

    ```json
    {
        "username": "newuser",
        "password": "password123"
    }
    ```

---

### Получение JWT-токена

- **URL:** `POST /api/token/`  
- **Пример запроса:**

    ```json
    {
        "username": "newuser",
        "password": "password123"
    }
    ```

- **Пример ответа:**

    ```json
    {
        "access": "<access_token>",
        "refresh": "<refresh_token>"
    }
    ```

---

### Создание задачи

- **URL:** `POST /api/tasks/create/`  
- **Пример запроса (суммирование чисел):**

    ```json
    {
        "task_type": "sum",
        "input_data": {
            "numbers": [1, 2, 3]
        }
    }
    ```

- **Пример запроса (обратный отсчёт):**

    ```json
    {
        "task_type": "countdown",
        "input_data": {
            "seconds": 5
        }
    }
    ```

---

### Получение списка задач

- **URL:** `GET /api/tasks/`  
- **Пример ответа:**

    ```json
    {
        "count": 2,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "task_type": "sum",
                "input_data": {"numbers": [1, 2, 3]},
                "status": "completed",
                "result": {"result": 6},
                "created_at": "2024-12-16T12:00:00Z"
            },
            {
                "id": 2,
                "task_type": "countdown",
                "input_data": {"seconds": 5},
                "status": "completed",
                "result": {"message": "Обратный отсчёт завершён"},
                "created_at": "2024-12-16T12:05:00Z"
            }
        ]
    }
    ```

---

### Просмотр статуса и результата задачи

- **URL:** `GET /api/tasks/<task_id>/`  
- **Пример ответа:**

    ```json
    {
        "id": 1,
        "task_type": "sum",
        "input_data": {"numbers": [1, 2, 3]},
        "status": "completed",
        "result": {"result": 6},
        "created_at": "2024-12-16T12:00:00Z"
    }
    ```
