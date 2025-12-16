from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List
import os
import time
from contextlib import asynccontextmanager

from database import get_db, init_db
from models import Movie
from schemas import MovieCreate, MovieUpdate, Movie as MovieSchema


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Жизненный цикл приложения FastAPI.
    Здесь выполняется логика при старте и остановке сервиса.
    """
    # Код, выполняемый при запуске приложения
    print("Инициализация базы данных...")
    max_retries = 10
    for i in range(max_retries):
        try:
            # Пытаемся инициализировать БД (проверка подключения + создание таблиц)
            init_db()
            print("База данных успешно инициализирована!")
            break
        except Exception as e:
            # Если не удалось — пробуем ещё несколько раз с паузами
            if i < max_retries - 1:
                print(f"Попытка подключения к БД {i+1}/{max_retries}: {e}")
                time.sleep(2)
            else:
                print(f"Ошибка инициализации БД: {e}")
    # Передаём управление самому приложению
    yield
    # Код, выполняемый при завершении работы приложения
    print("Приложение завершает работу...")


# Основной объект приложения FastAPI
app = FastAPI(title="Movie Collection Service", lifespan=lifespan)

# Статические файлы и шаблоны - должны быть определены перед роутами
try:
    # Монтируем папку со статикой по адресу /static
    app.mount("/static", StaticFiles(directory="static"), name="static")
except Exception as e:
    # Если статики нет — просто выводим предупреждение в консоль
    print(f"Предупреждение: не удалось смонтировать статические файлы: {e}")

# Подключаем Jinja2‑шаблоны из папки templates
templates = Jinja2Templates(directory="templates")


# ---------- API эндпоинты ----------

@app.get("/api/movies", response_model=List[MovieSchema])
def get_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получить список фильмов с пагинацией.
    Параметры skip/limit позволяют подгружать данные порциями.
    """
    movies = db.query(Movie).offset(skip).limit(limit).all()
    return movies


@app.get("/api/movies/{movie_id}", response_model=MovieSchema)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    """
    Получить один фильм по его идентификатору.
    """
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@app.post("/api/movies", response_model=MovieSchema)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    """
    Создать новый фильм.
    Данные приходят в теле запроса и валидируются через схему MovieCreate.
    """
    # Преобразуем Pydantic‑модель в dict и создаём ORM‑объект
    db_movie = Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)  # Обновляем объект, чтобы получить сгенерированный id и даты
    return db_movie


@app.put("/api/movies/{movie_id}", response_model=MovieSchema)
def update_movie(movie_id: int, movie: MovieUpdate, db: Session = Depends(get_db)):
    """
    Обновить существующий фильм по id.
    Поддерживается частичное обновление: передаются только изменяемые поля.
    """
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    # Берём только те поля, которые реально были переданы клиентом
    update_data = movie.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_movie, field, value)

    db.commit()
    db.refresh(db_movie)
    return db_movie


@app.delete("/api/movies/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    """
    Удалить фильм по id.
    """
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    db.delete(db_movie)
    db.commit()
    return {"message": "Movie deleted successfully"}


# ---------- Веб‑интерфейс ----------

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Главная страница с фронтендом (SPA на чистом JS),
    который ходит в API этого же сервера.
    """
    return templates.TemplateResponse("index.html", {"request": request})

