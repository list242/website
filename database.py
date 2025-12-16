from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/movie_db")

# Добавляем pool_pre_ping для автоматического переподключения
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={"connect_timeout": 10}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    try:
        # Проверяем подключение
        with engine.connect() as connection:
            from sqlalchemy import text
            connection.execute(text("SELECT 1"))
        # Создаём таблицы
        Base.metadata.create_all(bind=engine)
        print("Таблицы созданы успешно")
    except OperationalError as e:
        print(f"Ошибка подключения к БД: {e}")
        raise
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")
        raise

