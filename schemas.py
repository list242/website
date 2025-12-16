from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class MovieBase(BaseModel):
    """
    Базовая схема фильма для запросов/ответов API.
    Содержит общие поля, которые есть и при создании, и при чтении.
    """

    title: str = Field(..., min_length=1, max_length=200)
    director: Optional[str] = Field(None, max_length=100)
    year: Optional[int] = Field(None, ge=1888, le=2100)
    genre: Optional[str] = Field(None, max_length=50)
    rating: Optional[float] = Field(None, ge=0.0, le=10.0)
    description: Optional[str] = None


class MovieCreate(MovieBase):
    """
    Схема для создания фильма (тело POST‑запроса).
    Наследует все поля из MovieBase.
    """

    pass


class MovieUpdate(BaseModel):
    """
    Схема для частичного обновления фильма (тело PUT‑запроса).
    Все поля опциональные, чтобы можно было обновлять только часть данных.
    """

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    director: Optional[str] = Field(None, max_length=100)
    year: Optional[int] = Field(None, ge=1888, le=2100)
    genre: Optional[str] = Field(None, max_length=50)
    rating: Optional[float] = Field(None, ge=0.0, le=10.0)
    description: Optional[str] = None


class Movie(MovieBase):
    """
    Схема ответа API для фильма.
    Содержит базовые поля + служебные (id, даты создания/обновления).
    """

    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        # Разрешаем Pydantic создавать схему из ORM‑объектов SQLAlchemy (Movie модель)
        from_attributes = True

