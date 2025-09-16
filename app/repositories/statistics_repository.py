from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.operator_statistics import OperatorStatistics
from app.schemas.statistics import StatisticsItemCreate, StatisticsItemRead

from typing import List

from datetime import datetime


class StatisticsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get(self, request: StatisticsItemRead | List[int]) -> List[OperatorStatistics]:
        query = select(OperatorStatistics)

        if isinstance(request, list) and all(isinstance(i, int) for i in request) and request:
            query = query.where(OperatorStatistics.id.in_(request))
            result = await self.session.execute(query)
            return result.scalars().all()

        if request.shift_ids:
            query = query.where(OperatorStatistics.shift_id.in_(request.shift_ids))
        elif request.operator_ids:
            query = query.where(OperatorStatistics.operator_id.in_(request.operator_ids))

        if request.start_date:
            query = query.where(OperatorStatistics.stat_date >= request.start_date)

        if request.end_date:
            query = query.where(OperatorStatistics.stat_date <= request.end_date)

        if request.parameter_ids:
            query = query.where(OperatorStatistics.parameter_id.in_(request.parameter_ids))

        result = await self.session.execute(query)
        return result.scalars().all()

    async def create_statistics(self, request: StatisticsItemCreate) -> int:
        stat = OperatorStatistics(
            parameter_id=request.parameter_id,
            value=request.value,
            operator_id=request.operator_id,
            shift_id=request.shift_id,
            stat_date=datetime.now(),
        )
        self.session.add(stat)
        await self.session.flush()
        return stat.id
