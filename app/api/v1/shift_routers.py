from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.schemas.shifts import ShiftItemCreate, ShiftItemUpdate
from app.services.shifts import ShiftService
from app.services.break_shift import BreakShiftService
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/shifts", tags=["shifts"])


@router.post("/create")
async def create_shift_router(shift: ShiftItemCreate, session: AsyncSession = Depends(get_session)):
    service = ShiftService(session)
    try:
        async with session.begin():
            shift_id = await service.create_shift(shift)
        return {"status": "ok", "id": shift_id}
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(f"Error creating shift: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/close")
async def close_shift_router(shift: ShiftItemUpdate, session: AsyncSession = Depends(get_session)):
    service = ShiftService(session)
    break_sevice = BreakShiftService(session)
    try:
        async with session.begin():
            close_date = datetime.now()
            await break_sevice.close_unclosed_break_for_shift(shift.shift_id, close_date)
            await service.close_shift(shift, close_date)
        return {"status": "ok"}
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(f"Error updating shift: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def get_shift(operator_id: int, session: AsyncSession = Depends(get_session)):
    service = ShiftService(session)
    try:
        async with session.begin():
            shift = await service.get_shift_from_operator(operator_id)
        return {'shift': shift}
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(f"Error getting shift: {e}")
        raise HTTPException(status_code=500, detail=str(e))


