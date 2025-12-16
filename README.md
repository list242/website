# Website

REST API сервис на FastAPI с фронтенд интерфейсом.

## Описание

Веб-приложение для управления данными с использованием:
- **Backend**: FastAPI (асинхронный REST API)
- **Frontend**: HTML/CSS/JavaScript
- **Database**: SQLAlchemy ORM
- **Containerization**: Docker & Docker Compose

## Структура проекта

```
.
├── main.py              # Главное приложение FastAPI
├── models.py            # SQLAlchemy модели БД
├── schemas.py           # Pydantic схемы валидации
├── database.py          # Конфигурация базы данных
├── requirements.txt     # Зависимости Python
├── Dockerfile          # Конфигурация Docker контейнера
├── docker-compose.yml  # Orchestration контейнеров
├── templates/
│   └── index.html      # Главная страница
└── static/
    ├── style.css       # Стили
    └── script.js       # JavaScript логика
```

## Требования

- Python 3.9+
- Docker & Docker Compose (опционально)

## Установка

### Локально

1. **Клонируйте репозиторий**
```bash
git clone https://github.com/list242/website.git
cd website
```

2. **Создайте виртуальное окружение**
```bash
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
```

3. **Установите зависимости**
```bash
pip install -r requirements.txt
```

4. **Запустите приложение**
```bash
python main.py
```

Приложение будет доступно по адресу: **http://localhost:8000**

### С Docker

```bash
docker-compose up --build
```

Приложение будет доступно по адресу: **http://localhost:8000**

## API Endpoints

| Метод | Endpoint | Описание |
|-------|----------|---------|
| GET | `/` | Главная страница |
| GET | `/docs` | API документация (Swagger) |
| GET | `/redoc` | API документация (ReDoc) |

## Технологический стек

- **FastAPI** — современный веб-фреймворк
- **SQLAlchemy** — ORM для работы с БД
- **Pydantic** — валидация данных
- **Uvicorn** — ASGI сервер
- **Docker** — контейнеризация

## Разработка

```bash
# Обновить зависимости
pip freeze > requirements.txt

# Добавить новую зависимость
pip install package-name
pip freeze > requirements.txt

# Отправить изменения на GitHub
git add .
git commit -m "Описание изменений"
git push
```
## Контакты

GitHub: [@list242](https://github.com/list242)
