from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, distinct, update
from typing import List
from app.models.coefficient import Coefficient
from app.schemas.coefficients import CoefficientType, CoefficientItem


class CoefficientRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_coefficients(self):
        coefficients = await self.session.execute(select(Coefficient))
        coefficients = coefficients.scalars().all()
        return coefficients


    async def get_by_id(self, coef_id: int) -> Coefficient | None:
        return await self.session.get(Coefficient, coef_id)

    async def get_pos_neg_params(self, type: CoefficientType) -> List[str]:
        stmt = select(distinct(Coefficient.parameter)).where(Coefficient.type == type)
        result = await self.session.execute(stmt)
        return [row[0] for row in result.fetchall()]

    async def create_new_coefficient(self, item) -> Coefficient:
        coef = Coefficient(
            parameter=item.parameter,
            norm=item.norm,
            base=item.base,
            weight=0.0,
            type=item.type,
        )
        self.session.add(coef)
        await self.session.flush()
        return coef

    async def update_coefficients(self, coefficients: List[CoefficientItem]) -> None:
        for item in coefficients:
            stmt = (
                update(Coefficient)
                .where(
                    Coefficient.parameter == item.parameter,
                    Coefficient.type == item.type,
                )
                .values(
                    norm=item.norm,
                    base=item.base,
                    weight=item.weight,
                )
            )
            await self.session.execute(stmt)
