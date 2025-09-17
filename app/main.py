from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1 import employee_routers, coefficient_routers, shift_routers, break_shift_routers, statistics_routers, salary_routers
from app.core.database import init_models, shutdown_engine
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.jobs.salary_jobs import monthly_salary_job


scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init_models()
        scheduler.add_job(
            monthly_salary_job,
            CronTrigger(
                # day=1,
                hour=11,
                minute=0,
                timezone="Europe/Moscow"
            ),
            id="monthly_salary",
            replace_existing=True,
        )

        if scheduler.running is False:
            scheduler.start()

        yield
    except Exception as e:
        print(e)
    finally:
        scheduler.shutdown()
        await shutdown_engine()


app = FastAPI(title="Support Operators API", lifespan=lifespan)

app.include_router(employee_routers.router, prefix="/api/v1")
app.include_router(coefficient_routers.router, prefix="/api/v1")
app.include_router(shift_routers.router, prefix="/api/v1")
app.include_router(break_shift_routers.router, prefix="/api/v1")
app.include_router(statistics_routers.router, prefix="/api/v1")
app.include_router(salary_routers.router, prefix="/api/v1")





