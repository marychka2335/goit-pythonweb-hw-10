import asyncio
from sqlalchemy.ext.asyncio import create_async_engine


async def test_connection():
    # URL подключения с данными из вашего docker-compose.yml
    DATABASE_URL = "postgresql+asyncpg://myuser:mypassword@db:5433/mydatabase"

    # Создаем асинхронный движок
    engine = create_async_engine(DATABASE_URL)

    try:
        async with engine.connect() as conn:
            print("Connection successful!")  # Успешное подключение
    except Exception as e:
        print(f"Connection failed: {e}")  # Обработка ошибок
    finally:
        await engine.dispose()  # Закрываем соединение

# Запускаем асинхронный процесс
asyncio.run(test_connection())
