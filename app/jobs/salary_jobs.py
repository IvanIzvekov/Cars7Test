from app.services.salary import SalaryService
from app.core.database import get_session
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import asyncio


async def monthly_salary_job():
    async for session in get_session():
        async with session.begin():
            service = SalaryService(session)
            await service.calculate_prev_month_salary()
