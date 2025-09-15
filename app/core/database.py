import asyncio
import logging
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine
from sqlalchemy.exc import SQLAlchemyError, DBAPIError
from async_timeout import timeout
from app.models.base import Base
from app.core.config import settings


from app.models.employee import Employee
from app.models.coefficient import Coefficient
from app.models.shift import Shift
from app.models.break_shift import Break
from app.models.operator_statistics import OperatorStatistics
from app.models.salary_calculation import SalaryCalculation

logger = logging.getLogger(__name__)

engine: AsyncEngine = create_async_engine(
    f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
    f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}",
    echo=True,
    future=True
)

SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)


async def get_session():
    retries = settings.DB_GET_SESSION_RETRIES or 5
    delay = settings.DB_GET_SESSION_DELAY or 2.0
    timeout_sec = settings.DB_GET_SESSION_TIMEOUT or 10.0

    attempt = 0
    while attempt < retries:
        try:
            async with timeout(timeout_sec):
                async with SessionLocal() as session:
                    yield session
                    return
        except (SQLAlchemyError, DBAPIError, asyncio.TimeoutError) as e:
            attempt += 1
            logger.warning(f"Попытка {attempt}/{retries} сессии БД не удалась: {e}")
            await asyncio.sleep(delay)
    raise RuntimeError(f"Не удалось получить сессию БД после {retries} попыток")


async def init_models(retries: int = 5, delay: float = 2.0):
    attempt = 0
    while attempt < retries:
        try:
            async with timeout(delay):
                async with engine.begin() as conn:
                    await conn.run_sync(Base.metadata.create_all)
                logger.info("Таблицы успешно созданы")
                return
        except (SQLAlchemyError, DBAPIError) as e:
            attempt += 1
            logger.warning(f"Попытка {attempt}/{retries} создания таблиц не удалась: {e}")
            await asyncio.sleep(delay)
        raise RuntimeError(f"Не удалось создать таблицы после {retries} попыток")

async def shutdown_engine():
    try:
        await engine.dispose()
        logger.info("Движок БД закрыт корректно")
    except Exception as e:
        logger.error(f"Ошибка при закрытии движка: {e}")