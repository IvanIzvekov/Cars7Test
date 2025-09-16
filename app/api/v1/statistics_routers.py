from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session

from app.services.statistics import StatisticsService

from app.schemas.statistics import StatisticsItemRead, StatisticsItemCreate

import logging
from typing import List

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/statistics", tags=["statistics"])


@router.post("/get")
async def get_statistics_router(
        request: StatisticsItemRead,
        ids: List[int] | None = Query(None),
        session: AsyncSession = Depends(get_session)):
    service = StatisticsService(session)
    try:
        async with session.begin():
            if ids:
                statistics = await service.get_statistics(ids)
            else:
                statistics = await service.get_statistics(request)
        return {'statistics': statistics}
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create")
async def create_statistics_router(
        request: StatisticsItemCreate,
        session: AsyncSession = Depends(get_session)):
    service = StatisticsService(session)
    try:
        async with session.begin():
            statistics_id = await service.create_statistics(request)
        return {"status": "ok", "id": statistics_id}
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(f"Error creating statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))