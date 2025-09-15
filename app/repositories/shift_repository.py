from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, and_
import logging
from datetime import datetime
from app.models.shift import Shift
from app.schemas.shifts import ShiftItemCreate

logger = logging.getLogger(__name__)


class ShiftRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_shift(self, shift_id: int) -> Shift | None:
        """Получить смену по ID"""
        return await self.session.get(Shift, shift_id)

    async def get_shift_from_operator(self, operator_id: int) -> Shift | None:
        """Получить последнюю незакрытую смену по оператору"""
        stmt = (
            select(Shift)
            .where(
                and_(
                    Shift.operator_id == operator_id,
                    Shift.end_time == Shift.start_time,
                )
            )
            .order_by(desc(Shift.start_time))
            .limit(1)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_new_shift_in_db(self, operator_id: int) -> int:
        """Создать новую смену"""
        start_at = datetime.now()

        new_shift = Shift(
            start_time=start_at,
            end_time=start_at,
            operator_id=operator_id,
        )
        self.session.add(new_shift)

        await self.session.flush()
        return new_shift.id

    async def close_shift(self, shift: Shift, close_date: datetime):
        shift.end_time = close_date
