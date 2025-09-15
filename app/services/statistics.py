from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.statistics_repository import StatisticsRepository
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.shift_repository import ShiftRepository
from app.repositories.coefficient_repository import CoefficientRepository

from app.schemas.statistics import StatisticsItemCreate, StatisticsItemRead

from typing import List
from datetime import datetime

import logging

logger = logging.getLogger(__name__)


class StatisticsService:
    def __init__(self, session: AsyncSession):
        self.statistics_repository = StatisticsRepository(session)
        self.employee_repository = EmployeeRepository(session)
        self.shift_repository = ShiftRepository(session)
        self.coefficient_repository = CoefficientRepository(session)


    async def get_statistics(self, request: StatisticsItemRead | List[int]):
        return await self.statistics_repository.get(request)


    async def create_statistics(self, request: StatisticsItemCreate):
        if not await self.employee_repository.get_operator(request.operator_id):
            raise ValueError(f"Operator with id = {request.operator_id} not found")

        if not await self.shift_repository.get_shift(request.shift_id):
            raise ValueError(f"Shift with id = {request.shift_id} not found")

        if not await self.coefficient_repository.get_by_id(request.parameter_id):
            raise ValueError(f"Parameter with id = {request.parameter_id} not found")


        return await self.statistics_repository.create_statistics(request)
