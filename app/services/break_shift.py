from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from app.repositories.break_shift_repository import BreakShiftRepository
from app.repositories.shift_repository import ShiftRepository
from app.repositories.employee_repository import EmployeeRepository
from app.schemas.break_shift import BreakShiftItemCreate, BreakShiftItemClose
import logging

logger = logging.getLogger(__name__)


class BreakShiftService:
    def __init__(self, session: AsyncSession):
        self.repo = BreakShiftRepository(session)
        self.shift_repo = ShiftRepository(session)
        self.employee_repo = EmployeeRepository(session)

    async def get_break(self, shift_id: int):
        try:
            exist_shift = await self.shift_repo.get_shift(shift_id)
            if not exist_shift:
                raise ValueError(f"Shift with id = {shift_id} was not found")
            return await self.repo.get_break_shift_from_shift_id(shift_id)
        except Exception:
            logger.exception("Error while getting breaks")
            raise ValueError("Error while getting breaks")


    async def create_break(self, break_shift: BreakShiftItemCreate) -> int:
        try:
            if not await self.employee_repo.get_operator(break_shift.operator_id):
                raise ValueError(f"Operator with id = {break_shift.operator_id} not found")

            if not await self.shift_repo.get_shift(break_shift.shift_id):
                raise ValueError(f"Shift with id = {break_shift.shift_id} was not found")

            exist_break_shift = await self.repo.get_break_shift_from_shift_id(break_shift.shift_id)
            if exist_break_shift:
                raise ValueError(f"Break shift for shift with id = {break_shift.shift_id} already exists, break shift id = {exist_break_shift.id}")

            start_at = datetime.now()
            new_break = await self.repo.create_new_break_shift(
                shift_id=break_shift.shift_id,
                operator_id=break_shift.operator_id,
                start_time=start_at,
            )
            return new_break.id
        except Exception:
            logger.exception("Error while creating break")
            raise

    async def close_break(self, break_shift_id: int, end_time: datetime):
        try:
            break_shift = await self.repo.get_break_shift(break_shift_id)
            if not break_shift:
                raise ValueError(f"Break shift with id {break_shift_id} not found")
            await self.repo.close_break_shift(break_shift, end_time)
        except Exception:
            logger.exception("Error while closing break")
            raise

    async def close_unclosed_break_for_shift(self, shift_id: int, end_time: datetime):
        try:
            break_shift = await self.repo.get_break_shift_from_shift_id(shift_id=shift_id)
            if break_shift:
                await self.repo.close_break_shift(break_shift, end_time)
        except Exception:
            logger.exception("Error while closing unclosed break for shift")
            raise