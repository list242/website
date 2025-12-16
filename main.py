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
    # Startup
    print("Инициализация базы данных...")
    max_retries = 10
    for i in range(max_retries):
        try:
            init_db()
            print("База данных успешно инициализирована!")
            break
        except Exception as e:
            if i < max_retries - 1:
                print(f"Попытка подключения к БД {i+1}/{max_retries}: {e}")
                time.sleep(2)
            else:
                print(f"Ошибка инициализации БД: {e}")
    yield
    # Shutdown
    print("Приложение завершает работу...")


app = FastAPI(title="Movie Collection Service", lifespan=lifespan)

# Статические файлы и шаблоны - должны быть определены перед роутами
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except Exception as e:
    print(f"Предупреждение: не удалось смонтировать статические файлы: {e}")

templates = Jinja2Templates(directory="templates")

# API эндпоинты
@app.get("/api/movies", response_model=List[MovieSchema])
def get_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    movies = db.query(Movie).offset(skip).limit(limit).all()
    return movies

@app.get("/api/movies/{movie_id}", response_model=MovieSchema)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@app.post("/api/movies", response_model=MovieSchema)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    db_movie = Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@app.put("/api/movies/{movie_id}", response_model=MovieSchema)
def update_movie(movie_id: int, movie: MovieUpdate, db: Session = Depends(get_db)):
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    update_data = movie.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_movie, field, value)
    
    db.commit()
    db.refresh(db_movie)
    return db_movie

@app.delete("/api/movies/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    db.delete(db_movie)
    db.commit()
    return {"message": "Movie deleted successfully"}

# Веб-интерфейс
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

