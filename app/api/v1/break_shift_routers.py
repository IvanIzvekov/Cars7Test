from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.schemas.break_shift import BreakShiftItemCreate, BreakShiftItemClose
from app.services.break_shift import BreakShiftService
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/breaks", tags=["breaks"])


@router.post("/create")
async def create_break_router(
    break_shift: BreakShiftItemCreate,
    session: AsyncSession = Depends(get_session),
):
    service = BreakShiftService(session)
    try:
        async with session.begin():
            break_id = await service.create_break(break_shift)
        return {"status": "ok", "id": break_id}
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(f"Unexpected error while creating break: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")



@router.post("/close")
async def close_break_router(
    break_shift: BreakShiftItemClose,
    session: AsyncSession = Depends(get_session)
):
    service = BreakShiftService(session)
    try:
        async with session.begin():
            await service.close_break(break_shift.break_id, datetime.now())
        return {"status": "ok"}
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(f"Error closing break: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def get_breaks_router(shift_id: int, session: AsyncSession = Depends(get_session)):
    service = BreakShiftService(session)
    try:
        async with session.begin():
            breaks = await service.get_breaks(shift_id)
        return {'breaks': breaks}
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(f"Error getting breaks: {e}")
        raise HTTPException(status_code=500, detail=str(e))
