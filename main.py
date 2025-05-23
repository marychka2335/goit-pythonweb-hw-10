from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from src.database.db import get_db
from src.api import contacts  # імпортуємо наші маршрути для контактів


logger = logging.getLogger("uvicorn.error")

app = FastAPI(
    title="Contacts API",
    description="REST API для управління контактами",
    version="1.0",
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning("Validation error: %s", exc.errors())
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder(
            {
                "detail": exc.errors(),
                "message": "Помилка валідації. Перевірте передані дані.",
            }
        ),
    )


# Підключаємо маршрути контакту з префіксом /api
app.include_router(contacts.router, prefix="/api")


@app.get("/", response_model=dict)
async def read_root(request: Request):
    """
    Кореневий ендпоінт, що повертає повідомлення про версію додатку.
    """
    return {"message": "Contacts Application v1.0"}


@app.get("/api/healthchecker", response_model=dict)
async def healthchecker(db: AsyncSession = Depends(get_db)):
    """
    Ендпоінт для перевірки працездатності бази даних.
    Виконується простий запит до БД для перевірки з'єднання.
    """
    try:
        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database is not configured correctly",
            )
        return {"message": "Welcome to Contacts API!"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error connecting to the database",
        )
