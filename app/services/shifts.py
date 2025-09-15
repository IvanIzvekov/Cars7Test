from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import datetime
import logging

from app.repositories.shift_repository import ShiftRepository
from app.repositories.employee_repository import EmployeeRepository
from app.schemas.shifts import ShiftItemCreate, ShiftItemUpdate

logger = logging.getLogger(__name__)


class ShiftService:
    def __init__(self, session: AsyncSession):
        self.repo = ShiftRepository(session)
        self.employee_repo = EmployeeRepository(session)


    async def get_shift_from_operator(self, operator_id: int):
        try:
            if not await self.employee_repo.get_operator(operator_id):
                raise ValueError(f"Operator with id = {operator_id} not found")
            return await self.repo.get_shift_from_operator(operator_id)
        except Exception:
            logger.exception(f"Error getting last unclosed shift")
            raise

    async def create_shift(self, shift: ShiftItemCreate) -> int:
        try:
            if not await self.employee_repo.get_operator(shift.operator_id):
                raise ValueError(f"Operator with id = {shift.operator_id} not found")
            exist_shift = await self.repo.get_shift_from_operator(shift.operator_id)
            if exist_shift:
                raise ValueError(f"Operator with id = {shift.operator_id} already has unclosed shift, shift id = {exist_shift.id}")
            return await self.repo.create_new_shift_in_db(operator_id=shift.operator_id)
        except Exception:
            logger.exception(f"Error creating shift")
            raise

    async def close_shift(self, shift: ShiftItemUpdate, close_date: datetime):
        try:
            exist_shift = await self.repo.get_shift(shift.shift_id)

            if not exist_shift:
                raise ValueError(f"No unclosed shift for operator {shift.operator_id}")

            await self.repo.close_shift(exist_shift, close_date)
        except Exception:
            logger.exception(f"Error closing shift")
            raise
