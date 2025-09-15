from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from typing import List
import logging

from app.schemas.coefficients import CoefficientItem, CoefficientItemCreate, CoefficientType
from app.services.coefficients import CoefficientService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/coefficients", tags=["coefficients"])


@router.post("/create")
async def create_coefficients_router(
    request: CoefficientItemCreate,
    session: AsyncSession = Depends(get_session)
):
    if request.norm < request.base:
        raise HTTPException(status_code=400, detail="Normal value must be bigger then base")

    service = CoefficientService(session)
    try:
        async with session.begin():
            coef_id = await service.create_coefficient(request)
        return {"status": "ok", "id": coef_id}
    except ValueError as e:
        logger.exception(f"Validation error {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(f"Error creating coefficient: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/update")
async def update_coefficients_router(
    request: List[CoefficientItem],
    session: AsyncSession = Depends(get_session)
):
    service = CoefficientService(session)
    try:
        async with session.begin():
            allowed_params = {
                CoefficientType.POSITIVE: await service.get_positive_params(),
                CoefficientType.NEGATIVE: await service.get_negative_params()
            }

            await service.validate_coefficients(request, allowed_params)
            await service.update_coefficients(request)

        return {"status": "ok"}

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(f"Error updating coefficients: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def get_coefficients_router(
        session: AsyncSession = Depends(get_session)):
    service = CoefficientService(session)
    try:
        async with session.begin():
            coefficients = await service.get_coefficients()
        return {'coefficients': coefficients}
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(f"Error getting coefficients: {e}")
        raise HTTPException(status_code=500, detail=str(e))
