from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.services.salary import SalaryService
import logging
from typing import List


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/salary", tags=["salary"])


@router.get("/calculate_prev_month_salary")
async def create_break_router(
    operator_ids: List[int] = Query(None),
    session: AsyncSession = Depends(get_session),
):
    service = SalaryService(session)
    try:
        async with session.begin():
            await service.calculate_prev_month_salary(operator_ids)
        return {"status": "ok"}
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(f"Unexpected error while creating break: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
