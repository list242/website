from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import os

# URL подключения к базе данных.
# По умолчанию используется локальный PostgreSQL, но адрес можно переопределить
# через переменную окружения DATABASE_URL.
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/movie_db")

# Создаём движок SQLAlchemy.
# pool_pre_ping — проверка соединения перед использованием (чтобы не падать на "мертвых" коннектах).
# pool_recycle — периодическая пересборка коннектов.
# connect_args — дополнительные параметры подключения к драйверу.
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={"connect_timeout": 10}
)

# Фабрика сессий для работы с БД в рамках HTTP-запроса.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для всех ORM‑моделей.
Base = declarative_base()


def get_db():
    """
    Зависимость FastAPI, которая создаёт сессию БД на время запроса
    и гарантированно закрывает её после завершения.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Инициализация базы данных:
    - проверка доступности соединения;
    - создание всех таблиц, описанных в моделях.
    Вызывается на этапе запуска приложения.
    """
    try:
        # Проверяем подключение простым запросом
        with engine.connect() as connection:
            from sqlalchemy import text

            connection.execute(text("SELECT 1"))
        # Создаём таблицы по метаданным Base
        Base.metadata.create_all(bind=engine)
        print("Таблицы созданы успешно")
    except OperationalError as e:
        print(f"Ошибка подключения к БД: {e}")
        raise
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")
        raise

