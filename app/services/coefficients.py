from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import logging

from app.repositories.coefficient_repository import CoefficientRepository

from app.schemas.coefficients import CoefficientType, CoefficientItem, CoefficientItemCreate

logger = logging.getLogger(__name__)


class CoefficientService:
    def __init__(self, session: AsyncSession):
        self.repo = CoefficientRepository(session)
        self.session = session


    async def get_coefficients(self):
        try:
            return await self.repo.get_coefficients()
        except Exception:
            logger.exception(f"Error getting coefficients")
            raise

    async def validate_coefficients(self, coefficients: List[CoefficientItem], allowed_params: dict[CoefficientType, List[str]]):
        pos_params = []
        neg_params = []

        sum_coef_pos = 0
        sum_coef_neg = 0
        for coef in coefficients:
            if coef.parameter not in allowed_params[coef.type]:
                raise ValueError(f"Parameter {coef.parameter} is not allowed for type {coef.type}")
            else:
                pos_params.append(coef.parameter) if coef.type == CoefficientType.POSITIVE else neg_params.append(coef.parameter)
                sum_coef_pos += coef.weight if coef.type == CoefficientType.POSITIVE else 0
                sum_coef_neg += coef.weight if coef.type == CoefficientType.NEGATIVE else 0
            if coef.norm < coef.base:
                raise ValueError(f"Norm {coef.norm} is less than base {coef.base}")
            if coef.weight < 0 or coef.weight > 1:
                raise ValueError(f"Weight {coef.weight} is not in range [0, 1]")

        if len(pos_params) > 0 and len(pos_params) != len(allowed_params[CoefficientType.POSITIVE]):
            raise ValueError(f"Positive params count is not equal to allowed params count, allowed: {len(allowed_params[CoefficientType.POSITIVE])}, actual: {len(pos_params)}")
        else:
            if sum_coef_pos !=1 and len(pos_params) > 0:
                raise ValueError(f"Sum of positive coefficients is not equal to 1, actual: {sum_coef_pos}")
        if len(neg_params) > 0 and len(neg_params) != len(allowed_params[CoefficientType.NEGATIVE]):
            raise ValueError(f"Negative params count is not equal to allowed params count, allowed: {len(allowed_params[CoefficientType.NEGATIVE])}, actual: {len(neg_params)}")
        else:
            if sum_coef_neg != 1 and len(neg_params) > 0:
                raise ValueError(f"Sum of negative coefficients is not equal to 1, actual: {sum_coef_neg}")



    async def get_positive_params(self) -> List[str]:
        try:
            return await self.repo.get_pos_neg_params(CoefficientType.POSITIVE)
        except Exception:
            logger.exception(f"Error getting positive params")
            raise

    async def get_negative_params(self) -> List[str]:
        try:
            return await self.repo.get_pos_neg_params(CoefficientType.NEGATIVE)
        except Exception:
            logger.exception(f"Error getting negative params")
            raise

    async def create_coefficient(self, item: CoefficientItemCreate) -> int:
        try:
            coef = await self.repo.create_new_coefficient(item)
            return coef.id
        except Exception:
            logger.error(f"Error creating coefficient")
            raise

    async def update_coefficients(self, coefficients: List[CoefficientItem]) -> None:
        try:
            await self.repo.update_coefficients(coefficients)
        except Exception as e:
            logger.error(f"Error updating coefficients")
            raise

