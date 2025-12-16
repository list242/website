from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from sqlalchemy.sql import func
from database import Base


class Movie(Base):
    """
    ORM‑модель фильма.
    Описывает структуру таблицы `movies` в базе данных.
    """

    __tablename__ = "movies"

    # Первичный ключ
    id = Column(Integer, primary_key=True, index=True)
    # Обязательное название фильма
    title = Column(String(200), nullable=False, index=True)
    # Необязательные атрибуты записи
    director = Column(String(100))
    year = Column(Integer)
    genre = Column(String(50))
    rating = Column(Float)
    description = Column(Text)
    # Время создания и обновления записи (ставится/обновляется на стороне БД)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

