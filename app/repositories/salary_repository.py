from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.models.coefficient import Coefficient
from app.models.salary_calculation import SalaryCalculation
from datetime import datetime
from typing import List

class SalaryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def delete_salary_calculation(self, start_at: datetime, end_at: datetime, operator_ids: List[int] | None):
        query = delete(SalaryCalculation).where(
            SalaryCalculation.start_at >= start_at,
            SalaryCalculation.end_at <= end_at,
        )
        if operator_ids:
            query = query.where(SalaryCalculation.operator_id.in_(operator_ids))

        await self.session.execute(query)


    async def get_coefficients(self):
        """
        Получаем настройки коэффициентов (база, норма, вес)
        """
        query = select(Coefficient)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def save_salary_calculation(self, operator_id: int,
                                            parameter: str,
                                            value: float,
                                            total: float,
                                            salary_amount: float | None,
                                            start_at: datetime,
                                            end_at: datetime):

        calc = SalaryCalculation(
            operator_id=operator_id,
            parameter=parameter,
            value=value,
            total=total,
            salary_amount=salary_amount,
            start_at=start_at,
            end_at=end_at,
            calc_date=datetime.now()
        )

        self.session.add(calc)
