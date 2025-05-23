from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from src.conf.config import settings


def test_db_connection():
    # Отримуємо database_url з settings
    database_url = settings.database_url

    try:
        # Створюємо підключення до бази даних
        engine = create_engine(database_url)
        with engine.connect() as connection:
            # Виконуємо простий запит для перевірки підключення
            result = connection.execute(text("SELECT 1"))
            print(
                "Підключення до бази даних успішне! Результат тестового запиту:", result.scalar())

    except SQLAlchemyError as e:
        print("Помилка підключення до бази даних:", e)


if __name__ == "__main__":
    test_db_connection()
