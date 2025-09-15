from app.models.break_shift import Break
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc
from datetime import datetime


class BreakShiftRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_break_shift_from_shift_id(self, shift_id: int) -> Break | None:
        """Вернуть последнюю незакрытую паузу для смены"""
        stmt = (
            select(Break)
            .where(
                and_(
                    Break.shift_id == shift_id,
                    Break.end_time == Break.start_time,
                )
            )
            .order_by(desc(Break.start_time))
            .limit(1)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_new_break_shift(self, shift_id: int, operator_id: int, start_time: datetime) -> Break:
        """Создать новую паузу (без проверок)"""
        new_break = Break(
            start_time=start_time,
            end_time=start_time,
            shift_id=shift_id,
            operator_id=operator_id,
        )
        self.session.add(new_break)
        await self.session.flush()
        return new_break

    async def get_break_shift(self, break_shift_id: int) -> Break | None:
        """Получить паузу по ID"""
        return await self.session.get(Break, break_shift_id)

    async def close_break_shift(self, break_shift: Break, end_time: datetime) -> None:
        """Закрыть паузу (передать уже найденный объект)"""
        break_shift.end_time = end_time


